try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

from .modules.openmwplayer_paths import OpenMWPlayerPaths
from .modules.openmwplayer_settings import OpenMWPlayerSettings
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path

import os
import shutil
import mobase
import re

class OpenMWPlayer():
    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = OpenMWPlayerSettings(self.organiser)
        self.paths = OpenMWPlayerPaths(self.organiser, self.settings)
        self.utilities = SharedUtilities()
        super().__init__()

    _openMwExeNames = [
        "openmw.exe",
        "openmw-cs.exe",
        "openmw-launcher.exe",
        "openmw-wizard.exe"
    ]

    _settingsRegex = r"fallback=(?P<setting>[^,]*),(?P<value>[^\n]*)"

    def getCfgSettings(self, configPath):
        cfgSettings = {}
        with Path(configPath).open("r", encoding="utf-8-sig") as cfg:
            lines = cfg.readlines()
            for line in lines:
                match = re.match(self._settingsRegex, line)
                if match:
                    cfgSettings[match.groups()[0]] = match.groups()[1]
        return cfgSettings

    def runOpenMW(self, appName):
        appPath = Path(appName)
        fileName = appPath.name
        if fileName in self._openMwExeNames:
            # Export settings to OpenMW
            qInfo("OpenMWPlayer: OpenMW exe detected, exporting setup.")
            self.exportMOSetup()
            qInfo("OpenMWPlayer: OpenMW setup export complete.")

            # Run app separately.
            qInfo("OpenMWPlayer: Running selected exe.")
            os.startfile(appName)

            return False
        else:
            return True

    #TODO: Use the settings in plugins\data to replace all the fallback= settings in the config.
    def exportMOSetup(self):
        configPath = self.paths.openMWCfgPath()
        game = self.organiser.managedGame()
        self.clearCfg(configPath)

        profile = self.organiser.profile().name()
        groundCoverCustom = self.paths.openMwGrassSettingsPath(profile)
        groundCoverFiles = []
        if not groundCoverCustom.exists():
            with groundCoverCustom.open("x") as custNew:
                custNew.write("\n")
        with groundCoverCustom.open("r") as custGrnd:
            for line in custGrnd:
                line = line.replace("\n", "")
                if len(line) > 0:
                    groundCoverFiles.append(line)

        bsas = []
        rootBsa = filter(lambda x: x.lower().endswith(".bsa"), os.listdir(game.dataDirectory().absolutePath()))
        for bsa in rootBsa:
            bsas.append(bsa)

        with configPath.open("a", encoding="utf-8") as cfg:
            cfg.write(self.getDataString(game.dataDirectory().absolutePath()))
            mods = self.organiser.modList().allModsByProfilePriority(self.organiser.profile())
            for mod in mods:
                if (self.organiser.modList().state(mod) & 0x2) != 0:
                    modBsa = filter(lambda x: x.lower().endswith(".bsa") , os.listdir(self.organiser.modList().getMod(mod).absolutePath()))
                    for bsa in modBsa:
                        bsas.append(bsa)
                    self.writeDataString(cfg, mod)
            self.writeDataString(cfg, "Overwrite")

            pluginList = self.organiser.pluginList()
            plugins = pluginList.pluginNames()
            filtered = filter(lambda x: pluginList.loadOrder(x) >= 0, plugins)
            loadOrder = sorted(filtered, key=pluginList.loadOrder)
            groundCover = filter(lambda x: x in groundCoverFiles, plugins)
            for plugin in loadOrder:
                if plugin.endswith(".omwaddon.esp"):
                    cfg.write("content=" + plugin.replace(".omwaddon.esp", ".omwaddon") + "\n")
                elif plugin.endswith(".omwscripts.esp"):
                    cfg.write("content=" + plugin.replace(".omwscripts.esp", ".omwscripts") + "\n")
                else:
                    cfg.write("content=" + plugin + "\n")
            for ground in groundCover:
                if ground.endswith(".omwaddon.esp"):
                    cfg.write("groundcover=" + ground.replace(".omwaddon.esp", ".omwaddon") + "\n")
                elif ground.endswith(".omwscripts.esp"):
                    cfg.write("groundcover=" + ground.replace(".omwscripts.esp", ".omwscripts") + "\n")
                else:
                    cfg.write("groundcover=" + ground + "\n")
            for bsa in bsas:
                cfg.write("fallback-archive=" + bsa.split(os.path.sep)[-1] + "\n")

    def clearCfg(self, configPath):
        lines = []
        with configPath.open("r", encoding="utf-8-sig") as cfg:
            lines = cfg.readlines()
        with configPath.open("w", encoding="utf-8-sig") as cfg:
            for line in lines:
                if not line.startswith("data=") and not line.startswith("content=") and not line.startswith("groundcover=") and not line.startswith("fallback-archive="):
                    cfg.write(line)
            if len(lines) == 0 and not lines[-1].endswith("\n"):
                cfg.write("\n")
    
    def writeDataString(self, configFile, modName):
        configFile.write(self.getDataString(self.organiser.modList().getMod(modName).absolutePath()))

    def getDataString(self, dataPath):
        return "data=\"" + dataPath.replace("&", "&&").replace("\"", "&\"") + "\"\n"
        
    def createDummy(self, mod):
        # Identify any omwaddons and create a dummy esp for them.
        modData = self.organiser.modList().getMod(mod)
        modPath = modData.absolutePath()
        modChanged = False
        files = os.listdir(modPath)
        omwaddons = filter(lambda x: x.lower().endswith(".omwaddon"), files)
        dummySource = self.paths.dummyEspPath()
        for omwaddon in omwaddons:
            dummyPath = Path(modPath) / Path(str(omwaddon) + ".esp")
            if not dummyPath.exists():
                self.utilities.copyTo(dummySource, dummyPath)
                modChanged = True
        omwscripts = filter(lambda x: x.lower().endswith(".omwscripts"), files)
        for omwaddon in omwscripts:
            dummyPath = Path(modPath) / Path(str(omwaddon) + ".esp")
            if not dummyPath.exists():
                self.utilities.copyTo(dummySource, dummyPath)
                modChanged = True
        #if modChanged == True:
            #self.organiser.modDataChanged(modData)
        return modChanged

    def deleteDummy(self, mod):
        # Remove any dummy esp files from the mod.
        modData = self.organiser.modList().getMod(mod)
        modPath = modData.absolutePath()
        modChanged = False
        files = os.listdir(modPath)
        dummyfiles = filter(lambda x: x.lower().endswith(".omwaddon.esp"), files)
        clearSize = os.path.getsize(self.paths.dummyEspPath())
        for dummy in dummyfiles:
            dummyPath = Path(modPath) / Path(dummy)
            if os.path.getsize(dummyPath) == clearSize:
                self.utilities.deletePath(dummyPath)
                modChanged = True
        dummyscripts = filter(lambda x: x.lower().endswith(".omwscripts.esp"), files)
        for dummy in dummyscripts:
            dummyPath = Path(modPath) / Path(dummy)
            if os.path.getsize(dummyPath) == clearSize:
                self.utilities.deletePath(dummyPath)
                modChanged = True
        #if modChanged == True:
            #self.organiser.modDataChanged(modData)
        return modChanged

    def enableDummy(self):
        # Create dummy esp files for any omwaddons that currently exist.
        allMods = self.organiser.modList().allMods()
        refresh = False
        for mod in allMods:
            modChanged = self.createDummy(mod)
            if modChanged == True:
                refresh = True
        if refresh == True:
            self.organiser.refresh()
        
    def disableDummy(self):
        # Remove dummy esp files for any omwaddons that currently exist.
        allMods = self.organiser.modList().allMods()
        refresh = False
        for mod in allMods:
            modChanged = self.deleteDummy(mod)
            if modChanged == True:
                refresh = True
        if refresh == True:
            self.organiser.refresh()