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
        self.clearOpenMWCfg(configPath)

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

        # Migrated from OpenMWExport by AnyOldName3
        with configPath.open("a", encoding="utf-8") as openmwcfg:
            # write out data directories
            openmwcfg.write(self.addPath(game.dataDirectory().absolutePath()))
            for mod in self.organiser.modsSortedByProfilePriority():
                self.addMod(openmwcfg, mod)
            self.addMod(openmwcfg, "Overwrite")
            
            # write out content (plugin) files
            # order content files by load order
            loadOrder = {}
            for plugin in self.organiser.pluginList().pluginNames():
                loadIndex = self.organiser.pluginList().loadOrder(plugin)
                if loadIndex >= 0:
                    loadOrder[loadIndex] = plugin
                elif plugin in groundCoverFiles:
                    openmwcfg.write("groundcover=" + plugin + "\n")

            # actually write out the list
            for pluginIndex in range(len(loadOrder)):
                pluginName = loadOrder[pluginIndex]
                openmwcfg.write("content=" + pluginName + "\n")

    def clearOpenMWCfg(self, configPath):
        # Migrated from OpenMWExport by AnyOldName3
        tempFilePath = None
        with tempfile.NamedTemporaryFile(mode="w", delete = False, encoding="utf-8") as f:
            tempFilePath = f.name
            lastLine = ""
            with configPath.open("r", encoding="utf-8-sig") as openmwcfg:
                for line in openmwcfg:
                    if not line.startswith("data=") and not line.startswith("content=") and not line.startswith("groundcover="):
                        f.write(line)
                        lastLine = line
            # ensure the last line ended with a line break
            if not lastLine.endswith("\n"):
                f.write("\n")
        # we can't move to Path.replace due to https://bugs.python.org/issue29805
        os.remove(configPath)
        shutil.move(tempFilePath, configPath)
    
    def addMod(self, configFile, modName):
        # Migrated from OpenMWExport by AnyOldName3
        state = self.organiser.modList().state(modName)
        if (state & 0x2) != 0 or modName == "Overwrite":
            path = self.organiser.getMod(modName).absolutePath()
            configLine = self.addPath(path)
            configFile.write(configLine)

    def addPath(self, dataPath):
        # Migrated from OpenMWExport by AnyOldName3
        # boost::filesystem::path uses a weird format in order to round-trip being constructed from a stream correctly, even when quotation characters are in the path
        processedPath = "data=\""
        for character in dataPath:
            if character == '&' or character == '"':
                processedPath += "&"
            processedPath += character
        processedPath += "\"\n"
        return processedPath