try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

from .modules.openmwplayer_paths import OpenMWPlayerPaths
from .modules.openmwplayer_settings import OpenMWPlayerSettings
from pathlib import Path

import tempfile
import os
import shutil
import mobase

class OpenMWPlayer():
    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = OpenMWPlayerSettings(self.organiser)
        self.paths = OpenMWPlayerPaths(self.organiser, self.settings)
        super().__init__()

    _openMwExeNames = [
        "openmw.exe",
        "openmw-cs.exe",
        "openmw-launcher.exe",
        "openmw-wizard.exe"
    ]

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
                    modBsa = filter(lambda x: x.lower().endswith(".bsa") , os.listdir(self.organiser.getMod(mod).absolutePath()))
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
                cfg.write("content=" + plugin + "\n")
            for ground in groundCover:
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
        configFile.write(self.getDataString(self.organiser.getMod(modName).absolutePath()))

    def getDataString(self, dataPath):
        return "data=\"" + dataPath.replace("&", "&&").replace("\"", "&\"") + "\"\n"