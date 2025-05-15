import mobase, os
from pathlib import Path
from functools import cached_property
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from ....common.common_strings import CommonStrings
from ....common.common_qt import *

class OpenMWPlayerStrings(CommonStrings):
    """ OpenMW Player strings module, contains strings used by OpenMW Player. """

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings):
        self.settings = settings
        super().__init__(plugin, organiser) 

    @cached_property
    def defaultSettingsCfgUrl(self):
        return "https://raw.githubusercontent.com/OpenMW/openmw/master/files/settings-default.cfg"
    
    @cached_property
    def openMwExecutables(self):
        return [
            "openmw.exe",
            "openmw-cs.exe",
            "openmw-launcher.exe",
            "openmw-wizard.exe",
            "delta_plugin.exe",
            "delta_plugin.bat"
        ]
    
    @cached_property
    def openMWSupportedExecutables(self):
        return [
            "openmw.exe"
        ]
    
    def customSettingsCfgPath(self):
        profile = self._organiser.profile()
        if profile.localSettingsEnabled():
            return str(Path(self.moProfilesPath) / profile.name() / "settings.cfg")
        return str(Path(self.pluginDataPath) / "settings.cfg")
        
    def customOpenmwCfgPath(self):
        profile = self._organiser.profile()
        if profile.localSettingsEnabled():
            return str(Path(self.moProfilesPath) / profile.name() / "openmw.cfg")
        return str(Path(self.pluginDataPath) / "openmw.cfg")

    def localSavesPath(self):
        profile = self._organiser.profile()
        return str(Path(self.moProfilesPath) / profile.name() / "openmw")
    
    @cached_property
    def defaultSettingsCfgPath(self):
        return str(Path(self.pluginDataPath) / "settings-default.cfg")
    
    def openmwCfgPath(self) -> str:
        """ Gets the path to the openmw.cfg file. """
        # Grab the saved setting if there is one.
        settingPath = Path(self.settings.cfgpath())
        if settingPath.is_file():
            return str(settingPath)

        # Grab the default path if it exists.
        defaultLocation = Path(QStandardPaths.locate(qDocLocation, str(Path("My Games", "OpenMW", "openmw.cfg"))))
        if defaultLocation.is_file():
            self.settings.updateSetting("openmwcfgpath", str(defaultLocation))
            return str(defaultLocation)

        return None
    
    def settingsCfgPath(self) -> str:
        cfgPath = self.openmwCfgPath()
        if cfgPath == None:
            return None
        return str(Path(cfgPath).parent / "settings.cfg")
    
