import mobase, os, urllib.request, re
from pathlib import Path
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from .openmwplayer_strings import OpenMWPlayerStrings
from ....common.common_qt import *
from ....common.common_utilities import *
from ....common.common_log import CommonLog

class OpenMWPlayerFiles():
    """ OpenMW Player files module, handles reading and writing openmw.cfg and settings.cfg. """

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings, strings:OpenMWPlayerStrings, log:CommonLog):
        self._organiser = organiser
        self._settings = settings
        self._strings = strings
        self._log = log
        super().__init__(plugin, organiser) 

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
            cfgText.append(f"[{cfgGroup}]")
            for cfgKey in settingsCfg[cfgGroup]:
                cfgValue = settingsCfg[cfgGroup][cfgKey]
                cfgText.append(f"{cfgKey} = {cfgValue}")
        if saveLines(cfgPath, cfgText):
            self._log.debug(f"Saved {cfgPath}")
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

    def getCustomSettingsCfg(self, profile:str):
        """Gets the custom settings.cfg for a specific profile."""
        settingsCfgPath = self._strings.customSettingsCfgPath(profile)
        if Path(settingsCfgPath).exists():
            return self.readSettingsCfg(settingsCfgPath)
        return None
    
    def getSettingsCfg(self):
        """Gets the settings.cfg for the current installation of OpenMW."""
        settingsCfgPath = self._strings.settingsCfgPath()
        if Path(settingsCfgPath).exists():
            return self.readSettingsCfg(settingsCfgPath)
        return None
    
    def getCompleteSettingsCfg(self, profile:str):
        """Gets the full settings.cfg from a profile, merged with missing entries from default settings."""
        profileCfg = self.getCustomSettingsCfg(profile)
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
            lines = loadLines(cfgPath)
            for line in lines:
                fallbackMatch = re.match(self._openmwCfgRegex, line)
                archiveMatch =  re.match(self._openmwCfgBsaRegex, line)
                groundcoverMatch =  re.match(self._openmwCfgGroundRegex, line)
                contentMatch =  re.match(self._openmwCfgContentRegex, line)
                dataMatch =  re.match(self._openmwCfgDataRegex, line)
            return openmwCfg
        else:
            return None