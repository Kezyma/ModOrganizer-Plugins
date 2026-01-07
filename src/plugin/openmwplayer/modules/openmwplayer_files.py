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
    # Updated regex to handle optional spaces around '=' and empty values
    _settingsCfgSettingRegex = r"^(?P<setting>[^=\n#]+?)\s*=\s*(?P<value>[^\n]*)"
    _settingsCfgCommentRegex = r"^[#;]\s*(?P<comment>.*)"

    def readSettingsCfg(self, cfgPath:str):
        """Reads a settings.cfg into a dictionary with comments."""
        if Path(cfgPath).exists():
            settingsCfg = {}
            cfgLines = loadLines(cfgPath)
            cfgGroup = ""
            pendingComment = []

            for cfgLine in cfgLines:
                headingMatch = re.match(self._settingsCfgHeadingRegex, cfgLine)
                commentMatch = re.match(self._settingsCfgCommentRegex, cfgLine)
                settingMatch = re.match(self._settingsCfgSettingRegex, cfgLine)

                if headingMatch:
                    cfgGroup = headingMatch.groups()[0]
                    settingsCfg[cfgGroup] = {}
                    pendingComment = []
                elif commentMatch:
                    pendingComment.append(commentMatch.group("comment"))
                elif settingMatch and cfgGroup:
                    # Strip whitespace from setting name, preserve value as-is (including empty)
                    settingName = settingMatch.groups()[0].strip()
                    settingValue = settingMatch.groups()[1]
                    settingsCfg[cfgGroup][settingName] = {
                        "value": settingValue,
                        "comment": "\n".join(pendingComment) if pendingComment else ""
                    }
                    pendingComment = []
                elif not cfgLine.strip():
                    # Blank line resets pending comments
                    pendingComment = []
            return settingsCfg
        else:
            return None
        
    def saveSettingsCfg(self, cfgPath:str, settingsCfg:dict):
        """Saves a settings.cfg dictionary to a specific path, preserving comments."""
        cfgText = []
        for cfgGroup in settingsCfg:
            cfgText.append("\n")
            cfgText.append(f"[{cfgGroup}]\n")
            for cfgKey in settingsCfg[cfgGroup]:
                settingData = settingsCfg[cfgGroup][cfgKey]
                # Handle both old format (string) and new format (dict)
                if isinstance(settingData, dict):
                    comment = settingData.get("comment", "")
                    cfgValue = settingData.get("value", "")
                    if comment:
                        for line in comment.split("\n"):
                            cfgText.append(f"# {line}\n")
                else:
                    cfgValue = settingData
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
    
    def _getSettingValue(self, settingData) -> str:
        """Extract value from setting data (handles both string and dict formats)."""
        if isinstance(settingData, dict):
            return settingData.get("value", "")
        return settingData

    def _getSettingComment(self, settingData) -> str:
        """Extract comment from setting data (handles both string and dict formats)."""
        if isinstance(settingData, dict):
            return settingData.get("comment", "")
        return ""

    def getCompleteSettingsCfg(self):
        """Gets the full settings.cfg from a profile, merged with missing entries from default settings."""
        profileCfg = self.getCustomSettingsCfg()
        defaultCfg = self.getDefaultSettingsCfg()

        # If we have no default config, use profile config or empty dict
        if defaultCfg is None:
            return profileCfg if profileCfg is not None else {}

        # If we have no profile config, just return defaults
        if profileCfg is None:
            return defaultCfg

        # Merge profile config into default config
        # This preserves all default settings and overwrites with profile values where they exist
        for category in defaultCfg:
            if category in profileCfg:
                for setting in defaultCfg[category]:
                    if setting in profileCfg[category]:
                        # Use profile value (even if empty - user may have intentionally cleared it)
                        # Preserve comment from default if profile doesn't have one
                        profileData = profileCfg[category][setting]
                        defaultData = defaultCfg[category][setting]
                        profileValue = self._getSettingValue(profileData)
                        defaultComment = self._getSettingComment(defaultData)
                        profileComment = self._getSettingComment(profileData)
                        # Use profile comment if it has one, otherwise keep default comment
                        finalComment = profileComment if profileComment else defaultComment
                        defaultCfg[category][setting] = {
                            "value": profileValue,
                            "comment": finalComment
                        }

        # Also add any categories/settings from profile that aren't in defaults
        for category in profileCfg:
            if category not in defaultCfg:
                defaultCfg[category] = profileCfg[category]
            else:
                for setting in profileCfg[category]:
                    if setting not in defaultCfg[category]:
                        defaultCfg[category][setting] = profileCfg[category][setting]

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
            for ext in ["*.esp", "*.esm"]:
                globPattern = f"{folder}\\{ext}"
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
        t = threading.Thread(target=self.refreshOpenmwCfg, daemon=True)
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