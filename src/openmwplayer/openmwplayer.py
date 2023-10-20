try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

from .modules.openmwplayer_paths import OpenMWPlayerPaths
from .modules.openmwplayer_settings import OpenMWPlayerSettings
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path

import os, shutil, mobase, re, codecs, sys, urllib.request
from datetime import datetime, timedelta

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

    _openMwDefaultSettingsCfgUrl = "https://raw.githubusercontent.com/OpenMW/openmw/master/files/settings-default.cfg"

    _settingsRegex = r"fallback=(?P<setting>[^,]*),(?P<value>[^\n]*)"
    _settingsBsaRegex = r"fallback-archive=(?P<value>[^\n]*)"

    _settingsCfgHeadingRegex = r"\[(?P<title>[^\]]*)\]"
    _settingsCfgSettingRegex = r"^(?P<setting>[^=\n#]*)\s=\s(?P<value>[^\n]*)"

    def getCfgSettings(self, configPath):
        cfgSettings = {}
        with Path(configPath).open("r", encoding="utf-8-sig") as cfg:
            lines = cfg.readlines()
            for line in lines:
                match = re.match(self._settingsRegex, line)
                if match:
                    cfgSettings[match.groups()[0]] = match.groups()[1]
        return cfgSettings

    def getCfgBsaSettings(self, configPath):
        cfgSettings = []
        with Path(configPath).open("r", encoding="utf-8-sig") as cfg:
            lines = cfg.readlines()
            for line in lines:
                match = re.match(self._settingsBsaRegex, line)
                if match:
                    cfgSettings.append(match.groups()[0])
        return cfgSettings

    def getDefaultSettingsCfg(self):
        defaultCfgPath = self.paths.openMwDefaultSettingsCfgPath()
        if not defaultCfgPath.exists() or datetime.fromtimestamp(os.path.getmtime(str(defaultCfgPath))) < (datetime.today() - timedelta(days=1)):
            try:
                urllib.request.urlretrieve(self._openMwDefaultSettingsCfgUrl, defaultCfgPath)
            except:
                qInfo("Could not update OpenMW base settings.cfg")
        if defaultCfgPath.exists():
            defaultSettings = self.getSettingsCfgSettings(defaultCfgPath)
            return defaultSettings
        return {}

    def getSettingsCfgSettings(self, settingsCfgPath):
        settingsCfg = {}
        with Path(settingsCfgPath).open("r", encoding="utf-8") as cfg:
            lines = cfg.readlines()
            currentGroup = ""
            for line in lines:
                headingMatch = re.match(self._settingsCfgHeadingRegex, line)
                settingMatch = re.match(self._settingsCfgSettingRegex, line)
                if headingMatch:
                    currentGroup = headingMatch.groups()[0]
                    settingsCfg[currentGroup] = {}
                elif settingMatch:
                    settingsCfg[currentGroup][settingMatch.groups()[0]] = settingMatch.groups()[1]
        return settingsCfg
    
    def getCompleteSettingsCfg(self, settingsCfgPath):
        defaultSettings = self.getDefaultSettingsCfg()
        overrides = self.getSettingsCfgSettings(settingsCfgPath)
        for category in overrides:
            if category not in defaultSettings:
                defaultSettings[category] = {}
            for setting in overrides[category]:
                defaultSettings[category][setting] = overrides[category][setting]
        return defaultSettings

    def importOpenMWCfg(self, configPath):
        currentSettings = self.getCfgSettings(configPath)
        self.updateImportedSettings(currentSettings)
        currentBsas = self.getCfgBsaSettings(configPath)
        self.updateImportedBsas(currentBsas)

    def importOpenMwSettingsCfg(self, configPath):
        currentSettingsCfg = self.getCompleteSettingsCfg(configPath)
        self.updateImportedSettingsCfg(currentSettingsCfg)

    def updateImportedSettingsCfg(self, settings):
        profile = self.organiser.profile().name()
        existingPath = self.paths.openMWSavedSettingsCfgPath(profile)
        with Path(existingPath).open("w", encoding="utf-8") as settingscfg:
            for category in settings:
                settingscfg.write("\n[" + category + "]\n")
                for setting in settings[category]:
                    settingscfg.write(setting + " = " + settings[category][setting] + "\n")

    def updateImportedSettings(self, settings):
        profile = self.organiser.profile().name()
        existingPath = self.paths.openMwBaseCfgPath(profile)
        with Path(existingPath).open("w", encoding="utf-8-sig") as omwcfg:
            omwcfg.write("\n")
            for setting in settings:
                omwcfg.write("fallback=" + setting + "," + settings[setting] + "\n")

    def updateImportedBsas(self, settings):
        profile = self.organiser.profile().name()
        existingPath = self.paths.openMwBsaSettingsPath(profile)
        with Path(existingPath).open("w", encoding="utf-8-sig") as omwcfg:
            omwcfg.write("\n")
            for setting in settings:
                omwcfg.write(setting + "\n")

    def runImport(self, appName):
        appPath = Path(appName)
        fileName = appPath.name
        if fileName in self._openMwExeNames:
            qInfo("OpenMWPlayer: OpenMW exe closing, importing setup.")
            self.importAllConfigs()
        return True
    
    def importAllConfigs(self):
        configPath = self.paths.openMWCfgPath()
        settingsPath = self.paths.openMwSettingsCfgPath()
        self.importOpenMWCfg(configPath)
        self.importOpenMwSettingsCfg(settingsPath)

    def runOpenMW(self, appName):
        appPath = Path(appName)
        fileName = appPath.name
        #if fileName in self._openMwExeNames:
        #    qInfo("OpenMWPlayer: OpenMW exe detected, exporting setup.")
        #    self.runExport()
        #return True
        # Legacy Method.
        if fileName in self._openMwExeNames:
            qInfo("OpenMWPlayer: OpenMW exe detected, exporting setup.")
            self.runExport()

            # Run app separately.
            qInfo("OpenMWPlayer: Running selected exe.")
            os.startfile(appName)

            return False
        else:
            return True
        
    def runExport(self):
        # Export settings to OpenMW
        self.exportMOSetup()
        if self.settings.manageengine():
            self.exportMOSettingsSetup()
        qInfo("OpenMWPlayer: OpenMW setup export complete.")

    def exportMOSettingsSetup(self):
        profile = self.organiser.profile().name()
        outputPath = self.paths.openMwSettingsCfgPath()
        savedPath = self.paths.openMWSavedSettingsCfgPath(profile)
        if not Path(savedPath).exists():
            self.importOpenMwSettingsCfg(outputPath)

        self.utilities.deletePath(outputPath)
        self.utilities.copyTo(Path(savedPath), Path(outputPath))
        self.clearBOMFlag(str(outputPath))

    def exportMOSetup(self):
        profile = self.organiser.profile().name()
        configPath = self.paths.openMWCfgPath()
        settingsPath = self.paths.openMwBaseCfgPath(profile)
        if not Path(settingsPath).exists():
            self.importOpenMWCfg(configPath)

        game = self.organiser.managedGame()
        self.clearCfg(configPath)

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

        bsaCustom = self.paths.openMwBsaSettingsPath(profile)
        bsaFiles = []
        if not bsaCustom.exists():
            with bsaCustom.open("x") as custNew:
                custNew.write("\n")
        with bsaCustom.open("r") as custGrnd:
            for line in custGrnd:
                line = line.replace("\n", "")
                if len(line) > 0:
                    bsaFiles.append(line)

        baseSettings = self.getCfgSettings(settingsPath)

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

            bsaOrdered = []
            for bsaFile in bsaFiles:
                if bsaFile in bsas:
                    bsaOrdered.append(bsaFile)

            if self.settings.managesettings():
                for setting in baseSettings:
                    cfg.write("fallback=" + setting + "," + baseSettings[setting] + "\n")
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
            for bsa in bsaOrdered:
                cfg.write("fallback-archive=" + bsa.split(os.path.sep)[-1] + "\n")

    def clearCfg(self, configPath):
        lines = []
        with configPath.open("r", encoding="utf-8-sig") as cfg:
            lines = cfg.readlines()
        with configPath.open("w", encoding="utf-8-sig") as cfg:
            for line in lines:
                if not line.startswith("data=") and not line.startswith("content=") and not line.startswith("groundcover=") and not line.startswith("fallback-archive="):
                    if not self.settings.managesettings() or not line.startswith("fallback="):
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

    def clearBOMFlag(self, path):
        BUFSIZE = 4096
        BOMLEN = len(codecs.BOM_UTF8)
        with open(path, "r+b") as fp:
            chunk = fp.read(BUFSIZE)
            if chunk.startswith(codecs.BOM_UTF8):
                i = 0
                chunk = chunk[BOMLEN:]
                while chunk:
                    fp.seek(i)
                    fp.write(chunk)
                    i += len(chunk)
                    fp.seek(BOMLEN, os.SEEK_CUR)
                    chunk = fp.read(BUFSIZE)
                fp.seek(-BOMLEN, os.SEEK_CUR)
                fp.truncate()