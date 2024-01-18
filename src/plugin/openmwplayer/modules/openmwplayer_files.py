import mobase, os, urllib.request, re, glob, codecs, threading
from pathlib import Path
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from .openmwplayer_strings import OpenMWPlayerStrings
from ....common.common_qt import *
from ....common.common_utilities import *
from ....common.common_log import CommonLog

class OpenMWPlayerFiles():
    """ OpenMW Player files module, handles reading and writing openmw.cfg and settings.cfg. """

    def __init__(self, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings, strings:OpenMWPlayerStrings, log:CommonLog):
        self._organiser = organiser
        self._settings = settings
        self._strings = strings
        self._log = log

    _settingsCfgHeadingRegex = r"\[(?P<title>[^\]]*)\]"
    _settingsCfgSettingRegex = r"^(?P<setting>[^=\n#]*)\s=\s(?P<value>[^\n]*)"
    def readSettingsCfg(self, cfgPath:str):
        """Reads a settings.cfg into a dictionary."""
        if Path(cfgPath).exists():
            settingsCfg = {}
            cfgLines = loadLines(cfgPath)
            cfgGroup = ""
            for cfgLine in cfgLines:
                headingMatch = re.match(self._settingsCfgHeadingRegex, cfgLine)
                settingMatch = re.match(self._settingsCfgSettingRegex, cfgLine)
                if headingMatch:
                    cfgGroup = headingMatch.groups()[0]
                    settingsCfg[cfgGroup] = {}
                elif settingMatch:
                    settingsCfg[cfgGroup][settingMatch.groups()[0]] = settingMatch.groups()[1]
            return settingsCfg
        else:
            return None
        
    def saveSettingsCfg(self, cfgPath:str, settingsCfg:dict):
        """Saves a settings.cfg dictionary to a specific path."""
        cfgText = []
        for cfgGroup in settingsCfg:
            cfgText.append("\n")
            cfgText.append(f"[{cfgGroup}]\n")
            for cfgKey in settingsCfg[cfgGroup]:
                cfgValue = settingsCfg[cfgGroup][cfgKey]
                cfgText.append(f"{cfgKey} = {cfgValue}\n")
        if saveLines(cfgPath, cfgText):
            self._log.debug(f"Saved {cfgPath}")
            self.clearBOMFlag(cfgPath)
        else:
            self._log.info(f"Could not save {cfgPath}")

    def getDefaultSettingsCfg(self):
        """Gets the global default settings.cfg, or downloads it from github if it doesn't exist."""
        settingsCfgPath = self._strings.defaultSettingsCfgPath
        if not Path(settingsCfgPath).exists():
            settingsCfgUrl = self._strings.defaultSettingsCfgUrl
            try:
                urllib.request.urlretrieve(settingsCfgUrl, settingsCfgPath)
            except:
                self._log.info("Could not download base settings.cfg")
        return self.readSettingsCfg(settingsCfgPath)

    def getCustomSettingsCfg(self):
        """Gets the custom settings.cfg for a specific profile."""
        settingsCfgPath = self._strings.customSettingsCfgPath()
        if Path(settingsCfgPath).exists():
            return self.readSettingsCfg(settingsCfgPath)
        return None
    
    def getSettingsCfg(self):
        """Gets the settings.cfg for the current installation of OpenMW."""
        settingsCfgPath = self._strings.settingsCfgPath()
        if Path(settingsCfgPath).exists():
            return self.readSettingsCfg(settingsCfgPath)
        return None
    
    def getCompleteSettingsCfg(self):
        """Gets the full settings.cfg from a profile, merged with missing entries from default settings."""
        profileCfg = self.getCustomSettingsCfg()
        defaultCfg = self.getDefaultSettingsCfg()
        # Overwrite all default config values with ones from the profile.
        if profileCfg != None and defaultCfg != None:
            for key in defaultCfg:
                if key in profileCfg:
                    for setting in defaultCfg[key]:
                        if setting in profileCfg[key]:
                            defaultCfg[key][setting] = profileCfg[key][setting]
        return defaultCfg

    _openmwCfgRegex = r"fallback=(?P<setting>[^,]*),(?P<value>[^\n]*)"
    _openmwCfgBsaRegex = r"fallback-archive=(?P<value>[^\n]*)"
    _openmwCfgGroundRegex = r"groundcover=(?P<value>[^\n]*)"
    _openmwCfgContentRegex = r"content=(?P<value>[^\n]*)"
    _openmwCfgDataRegex = r"data=(?P<value>[^\n]*)"
    def readOpenmwCfg(self, cfgPath:str):
        """Reads an openmw.cfg into a dictionary."""
        if Path(cfgPath).exists():
            openmwCfg = {}
            openmwCfg["Archives"] = []
            openmwCfg["Groundcover"] = []
            openmwCfg["Content"] = []
            openmwCfg["Data"] = []
            openmwCfg["Settings"] = {}
            openmwCfg["Extra"] = []
            lines = loadLines(cfgPath)
            for line in lines:
                fallbackMatch = re.match(self._openmwCfgRegex, line)
                archiveMatch =  re.match(self._openmwCfgBsaRegex, line)
                groundcoverMatch =  re.match(self._openmwCfgGroundRegex, line)
                contentMatch =  re.match(self._openmwCfgContentRegex, line)
                dataMatch =  re.match(self._openmwCfgDataRegex, line)
                if fallbackMatch:
                    openmwCfg["Settings"][fallbackMatch.groups()[0]] = fallbackMatch.groups()[1]
                elif archiveMatch:
                    openmwCfg["Archives"].append(archiveMatch.groups()[0])
                elif groundcoverMatch:
                    openmwCfg["Groundcover"].append(groundcoverMatch.groups()[0])
                elif contentMatch:
                    openmwCfg["Content"].append(contentMatch.groups()[0])
                elif dataMatch:
                    openmwCfg["Data"].append(dataMatch.groups()[0])
                else:
                    openmwCfg["Extra"].append(line)
            return openmwCfg   
        else:
            return None
        
    def saveOpenmwCfg(self, cfgPath:str, openmwCfg:dict):
        """Saves an openmw.cfg dictionary to the specified path."""
        cfgText = []
        for setting in openmwCfg["Settings"]:
            settingValue = openmwCfg["Settings"][setting]
            cfgText.append(f"fallback={setting},{settingValue}\n")
        for setting in openmwCfg["Archives"]:
            if len(setting) > 0:
                cfgText.append(f"fallback-archive={setting}\n")
        for setting in openmwCfg["Data"]:
            if len(setting) > 0:
                cleanedPath = setting.replace("\\", "/").replace("&", "&&").replace("\"", "&\"")
                cfgText.append(f"data=\"{cleanedPath}\"\n")
        for setting in openmwCfg["Content"]:
            if len(setting) > 0:
                cfgText.append(f"content={setting}\n")
        for setting in openmwCfg["Groundcover"]:
            if len(setting) > 0:
                cfgText.append(f"groundcover={setting}\n")
        for setting in openmwCfg["Extra"]:
            if len(setting) > 0:
                cfgText.append(f"{setting}\n")
        if saveLines(cfgPath, cfgText):
            self._log.debug(f"Saved {cfgPath}")
        else:
            self._log.info(f"Could not save {cfgPath}")
        
    def getOpenmwCfg(self):
        openmwCfgPath = self._strings.openmwCfgPath()
        if Path(openmwCfgPath).exists():
            return self.readOpenmwCfg(openmwCfgPath)
        return None
    
    def getCustomOpenmwCfg(self):
        openmwCfgPath = self._strings.customOpenmwCfgPath()
        if Path(openmwCfgPath).exists():
            return self.readOpenmwCfg(openmwCfgPath)
        return None
    
    def getDataFolders(self):
        dataFolders = []
        dataFolders.append(self._strings.gameDataPath)
        modList = self._organiser.modList().allModsByProfilePriority(self._organiser.profile())
        for mod in modList:
            if self._organiser.modList().state(mod.encode('utf-16','surrogatepass').decode('utf-16')) & mobase.ModState.ACTIVE:
                modPath = Path(self._strings.moModsPath) / mod
                dataFolders.append(str(modPath))
        dataFolders.append(self._strings.moOverwritePath)
        return dataFolders
    
    def getEnabledPlugins(self):
        contentList = []
        pluginList = self._organiser.pluginList()
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
        return contentList
    
    def getArchiveOptions(self):
        dataFolders = self.getDataFolders()
        archives = []
        for folder in dataFolders:
            globPattern = f"{folder}\\*.bsa"
            matches = glob.glob(globPattern)
            for match in matches:
                archives.append(os.path.basename(match))
        return archives
    
    def getGroundcoverOptions(self):
        dataFolders = self.getDataFolders()
        content = []
        for folder in dataFolders:
            globPattern = f"{folder}\\*.esp"
            matches = glob.glob(globPattern)
            for match in matches:
                content.append(os.path.basename(match))
        return content
    
    _refreshInProgress = False
    def refreshOpenmwCfg(self):
        if not self._refreshInProgress:
            self._refreshInProgress = True
            currentCfg = self.getCustomOpenmwCfg()
            if currentCfg != None:
                currentCfg["Data"] = self.getDataFolders()
                currentCfg["Content"] = self.getEnabledPlugins()
                validArchives = self.getArchiveOptions()
                validGroundcover = self.getGroundcoverOptions()
                currentCfg["Archives"] = list(filter(lambda archive: archive in validArchives, currentCfg["Archives"]))
                currentCfg["Groundcover"] = list(filter(lambda groundcover: groundcover in validGroundcover, currentCfg["Groundcover"]))
                self.saveOpenmwCfg(self._strings.customOpenmwCfgPath(), currentCfg)
            self._refreshInProgress = False
        
    def refreshOpenmwCfgAsync(self):
        t = threading.Thread(target=self.refreshOpenmwCfgAsync, daemon=True)
        t.start()

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