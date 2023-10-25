try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

from .modules.openmwplayer_paths import OpenMWPlayerPaths
from .modules.openmwplayer_settings import OpenMWPlayerSettings
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path

import os, shutil, mobase, re, codecs, sys, urllib.request, subprocess, asyncio, threading
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
    _openMwExeSupport = [
        "openmw.exe"
    ]

    _openMwDefaultSettingsCfgUrl = "https://raw.githubusercontent.com/OpenMW/openmw/master/files/settings-default.cfg"

    _settingsRegex = r"fallback=(?P<setting>[^,]*),(?P<value>[^\n]*)"
    _settingsBsaRegex = r"fallback-archive=(?P<value>[^\n]*)"
    _settingsGroundRegex = r"groundcover=(?P<value>[^\n]*)"
    _settingsContentRegex = r"content=(?P<value>[^\n]*)"
    _settingsDataRegex = r"data=(?P<value>[^\n]*)"

    _settingsCfgHeadingRegex = r"\[(?P<title>[^\]]*)\]"
    _settingsCfgSettingRegex = r"^(?P<setting>[^=\n#]*)\s=\s(?P<value>[^\n]*)"

    def newInitialSetup(self):
        customPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        if not Path(customPath).exists():
            self.newImportOpenMwCfg()
            self.newImportSettingsCfg()
        self.newMigrateLegacy()

    def newMigrateLegacy(self):
        profile = self.organiser.profile().name()
        # Import and remove prior bsa settings.
        bsaPath = Path(self.paths.openMwBsaSettingsPath(profile))
        if bsaPath.exists():
            bsaFiles = self.newReadAllLines(bsaPath)
            toUpdate = []
            for file in bsaFiles:
                if file != "" and file != "\n":
                    toUpdate.append(file.replace("\n", ""))
            self.newUpdateOpenMwCfgArchives(toUpdate)
            self.utilities.deletePath(bsaPath)
        # Import and remove prior groundcover settings.
        grndPath = Path(self.paths.openMwGrassSettingsPath(profile))
        if grndPath.exists():
            grndFiles = self.newReadAllLines(grndPath)
            toUpdate = []
            for file in grndFiles:
                if file != "" and file != "\n":
                    toUpdate.append(file.replace("\n", ""))
            self.newUpdateOpenMwCfgGroundcover(toUpdate)
            self.utilities.deletePath(grndPath)
        # Load and import the existing settings.
        setPath = Path(self.paths.openMwBaseCfgPath(profile))
        if setPath.exists():
            oldSettings = self.getCfgSettings(setPath)
            self.newUpdateOpenMwCfgSettings(oldSettings)
            self.utilities.deletePath(setPath)
        # Load and import the existing settings.cfg data.
        setCfgPath = Path(self.paths.openMWSavedSettingsCfgPath(profile))
        if setCfgPath.exists():
            oldSettings = self.getCompleteSettingsCfg(setCfgPath)
            self.newUpdateSettingsCfgSettings(oldSettings)
            self.utilities.deletePath(setCfgPath)


    def newImportOpenMwCfg(self):
        configPath = self.paths.openMWCfgPath()
        if Path(configPath).exists():
            customPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
            qInfo("Copying: " + str(configPath) + " to " + str(customPath))
            self.utilities.copyTo(Path(configPath), Path(customPath))
        self.newRefreshContentAndData()

    def newImportSettingsCfg(self):
        configPath = self.paths.openMwSettingsCfgPath()
        if Path(configPath).exists():
            customPath = self.paths.openMwCustomSettingsCfgPath(self.organiser.profile().name())
            qInfo("Copying: " + str(configPath) + " to " + str(customPath))
            self.utilities.copyTo(Path(configPath), Path(customPath))
        # Make sure we have every possible setting.
        defaults = self.getDefaultSettingsCfg()
        overrides = self.newLoadSettingsCfgSettings()
        for category in overrides:
            if category not in defaults:
                defaults[category] = {}
            for setting in overrides[category]:
                defaults[category][setting] = overrides[category][setting]
        self.newUpdateSettingsCfgSettings(defaults)


    def newLoadOpenMwCfgSettings(self):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        cfgSettings = {}
        if Path(configPath).exists():
            with Path(configPath).open("r", encoding="utf-8-sig") as cfg:
                lines = cfg.readlines()
                for line in lines:
                    match = re.match(self._settingsRegex, line)
                    if match:
                        cfgSettings[match.groups()[0]] = match.groups()[1]
        return cfgSettings
    
    def newLoadOpenMwCfgArchives(self):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        cfgSettings = []
        if Path(configPath).exists():
            with Path(configPath).open("r", encoding="utf-8-sig") as cfg:
                lines = cfg.readlines()
                for line in lines:
                    match = re.match(self._settingsBsaRegex, line)
                    if match:
                        cfgSettings.append(match.groups()[0])
        return cfgSettings

    def newLoadOpenMwCfgGroundcover(self):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        cfgSettings = []
        if Path(configPath).exists():
            with Path(configPath).open("r", encoding="utf-8-sig") as cfg:
                lines = cfg.readlines()
                for line in lines:
                    match = re.match(self._settingsGroundRegex, line)
                    if match:
                        cfgSettings.append(match.groups()[0])
        return cfgSettings

    def newLoadSettingsCfgSettings(self):
        configPath = self.paths.openMwCustomSettingsCfgPath(self.organiser.profile().name())
        settingsCfg = {}
        if Path(configPath).exists():
            with Path(configPath).open("r", encoding="utf-8") as cfg:
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

    def newUpdateOpenMwCfgSettings(self, newSettings):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        newLines = []
        for setting in newSettings:
            newLines.append("fallback=" + setting + "," + newSettings[setting])
        self.newReplaceCfgLines(configPath, "fallback=", newLines)

    def newUpdateOpenMwCfgArchives(self, newArchives):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        newLines = []
        for archive in newArchives:
            newLines.append("fallback-archive=" + archive)
        self.newReplaceCfgLines(configPath, "fallback-archive=", newLines)

    def newUpdateOpenMwCfgGroundcover(self, newGroundcover):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        newLines = []
        for esp in newGroundcover:
            newLines.append("groundcover=" + esp)
        self.newReplaceCfgLines(configPath, "groundcover=", newLines)

    def newUpdateOpenMwCfgContent(self, newContent):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        newLines = []
        for esp in newContent:
            newLines.append("content=" + esp)
        self.newReplaceCfgLines(configPath, "content=", newLines)

    def newUpdateOpenMwCfgData(self, newData):
        configPath = self.paths.openMwCustomOpenMwCfgPath(self.organiser.profile().name())
        newLines = []
        for dir in newData:
            newLines.append("data=\"" + dir.replace("&", "&&").replace("\"", "&\"") + "\"")
        self.newReplaceCfgLines(configPath, "data=", newLines)

    def newUpdateSettingsCfgSettings(self, newSettings):
        configPath = self.paths.openMwCustomSettingsCfgPath(self.organiser.profile().name())
        with Path(configPath).open("w", encoding="utf-8") as settingscfg:
            for category in newSettings:
                settingscfg.write("\n[" + category + "]\n")
                for setting in newSettings[category]:
                    settingscfg.write(setting + " = " + newSettings[category][setting] + "\n")
        self.clearBOMFlag(configPath)

    def newExportOpenMwCfg(self):
        profile = self.organiser.profile().name()
        source = self.paths.openMwCustomOpenMwCfgPath(profile)
        destination = self.paths.openMWCfgPath()
        self.utilities.copyTo(source, destination)

    def newExportSettingsCfg(self):
        profile = self.organiser.profile().name()
        source = self.paths.openMwCustomSettingsCfgPath(profile)
        destination = self.paths.openMwSettingsCfgPath()
        self.utilities.copyTo(source, destination)

    def newReadAllLines(self, configPath):
        lines = []
        with configPath.open("r", encoding="utf-8-sig") as cfg:
            lines = cfg.readlines()
        return lines

    def newReplaceCfgLines(self, configPath, linePrefix, newLines):
        lines = self.newReadAllLines(configPath)
        with configPath.open("w", encoding="utf-8-sig") as cfg:
            for line in lines:
                if not line.startswith(linePrefix):
                    cfg.write(line)
            for newLine in newLines:
                cfg.write(newLine + "\n")
            if len(lines) == 0 and not lines[-1].endswith("\n"):
                cfg.write("\n")

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

    def newRunOpenMw(self, appName):
        appPath = Path(appName)
        fileName = appPath.name
        # Legacy Method.
        if fileName in self._openMwExeNames:
            # Run app separately.
            qInfo("OpenMWPlayer: Running selected exe.")
            t = threading.Thread(target=self.newRunOpenMWAsync, args=[appName], daemon=True)
            t.start()

            return False
        else:
            return True

    def newRunOpenMWAsync(self, appName):
        appPath = Path(appName)
        fileName = appPath.name
        if fileName in self._openMwExeSupport:
            configLocation = self.paths.openMwCustomSettingsPath(self.organiser.profile().name())
            args = [ appName, "--replace", "config", "--config", "\"" + str(configLocation) + "\"" ]
            if self.organiser.profile().localSavesEnabled():
                userdataLocation = configLocation / "openmw"
                args.append("--replace")
                args.append("user-data")
                args.append("--user-data")
                args.append("\"" + str(userdataLocation) + "\"")
            subprocess.call(args)
        else:
            openMwCfgPath = self.paths.openMWCfgPath()
            settingsCfgPath = self.paths.openMwSettingsCfgPath()

            if Path(openMwCfgPath).exists():
                self.utilities.copyTo(Path(openMwCfgPath), Path(str(openMwCfgPath) + ".omwpbackup"))
            if Path(settingsCfgPath).exists():
                self.utilities.copyTo(Path(settingsCfgPath), Path(str(settingsCfgPath) + ".omwpbackup"))
            self.newExportOpenMwCfg()
            self.newExportSettingsCfg()

            subprocess.call(appName)

            self.newImportOpenMwCfg()
            self.newImportSettingsCfg()
            if Path(str(openMwCfgPath) + ".omwpbackup").exists():
                self.utilities.moveTo(Path(str(openMwCfgPath) + ".omwpbackup"), Path(openMwCfgPath))
            if Path(str(settingsCfgPath) + ".omwpbackup").exists():
                self.utilities.moveTo(Path(str(settingsCfgPath) + ".omwpbackup"), Path(settingsCfgPath))
        qInfo("OpenMWPlayer: Closing selected exe.")

    def newGenerateDataList(self):
        dataList = []
        # Add the game folder.
        dataList.append(self.organiser.managedGame().dataDirectory().absolutePath())

        # Add the mod folders.
        mods = self.organiser.modList().allModsByProfilePriority(self.organiser.profile())
        for mod in mods:
            if (self.organiser.modList().state(mod) & 0x2) != 0:
                dataList.append(self.organiser.modList().getMod(mod).absolutePath())
        
        # Add the overwrite folder.
        dataList.append(self.organiser.modList().getMod("Overwrite").absolutePath())

        # Update the stored cfg.
        self.newUpdateOpenMwCfgData(dataList)

    def newGenerateContentList(self):
        contentList = []
        pluginList = self.organiser.pluginList()
        plugins = pluginList.pluginNames()
        filtered = filter(lambda x: pluginList.loadOrder(x) >= 0, plugins)
        loadOrder = sorted(filtered, key=pluginList.loadOrder)
        for plugin in loadOrder:
            if plugin.endswith(".omwaddon.esp"):
                contentList.append(plugin.replace(".omwaddon.esp", ".omwaddon"))
            elif plugin.endswith(".omwscripts.esp"):
                contentList.append(plugin.replace(".omwscripts.esp", ".omwscripts"))
            else:
                contentList.append(plugin)
        self.newUpdateOpenMwCfgContent(contentList)

    def newRefreshContentAndData(self):
        self.newGenerateDataList()
        self.newGenerateContentList()

# Obsolete!

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
        # Legacy Method.
        if fileName in self._openMwExeNames:
            qInfo("OpenMWPlayer: OpenMW exe detected, exporting setup.")
            self.runExport()

            # Run app separately.
            qInfo("OpenMWPlayer: Running selected exe.")
            t = threading.Thread(target=self.runOpenMWAsync, args=[appName], daemon=True)
            t.start()

            return False
        else:
            return True
        
    def runOpenMWAsync(self, appName):
        subprocess.call(appName)
        qInfo("OpenMWPlayer: Closing selected exe.")
        self.runImport(appName)
    
    def runExport(self):
        # Export settings to OpenMW
        self.exportMOSetup()
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
                    if not line.startswith("fallback="):
                        cfg.write(line)
            if len(lines) == 0 and not lines[-1].endswith("\n"):
                cfg.write("\n")
    
    def writeDataString(self, configFile, modName):
        configFile.write(self.getDataString(self.organiser.modList().getMod(modName).absolutePath()))

    def getDataString(self, dataPath):
        return "data=\"" + dataPath.replace("&", "&&").replace("\"", "&\"") + "\"\n"
