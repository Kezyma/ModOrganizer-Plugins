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

    @cached_property
    def defaultOpenmwCfgPath(self) -> str:
        """Gets the path to the bundled default openmw.cfg template."""
        return str(Path(__file__).parent.parent / "data" / "openmw_default.cfg")

    @cached_property
    def defaultOpenmwCfgFolder(self) -> str:
        """Gets the default OpenMW config folder path (Documents/My Games/OpenMW/)."""
        return str(Path(QStandardPaths.writableLocation(qDocLocation)) / "My Games" / "OpenMW")

    def defaultExternalOpenmwCfgPath(self) -> str:
        """Gets the default external openmw.cfg path (may not exist yet)."""
        return str(Path(self.defaultOpenmwCfgFolder) / "openmw.cfg")

    def openmwCfgPath(self) -> str:
        """Gets the path to the external openmw.cfg file.

        Resolution order:
        1. User-specified path in settings (if set and exists)
        2. Default system location (Documents/My Games/OpenMW/openmw.cfg)

        Always returns a valid path string (never None). The file may or may not
        exist - callers should check existence when needed.
        """
        # Check for user-specified path (not the placeholder)
        settingValue = self.settings.cfgpath()
        placeholder = "/Path/To/OpenMW/openmw.cfg"

        # If user has set a custom path (not placeholder, not empty)
        if settingValue and settingValue != placeholder and settingValue.strip():
            settingPath = Path(settingValue)
            if settingPath.is_file():
                return str(settingPath)

        # Return default location (may or may not exist)
        return self.defaultExternalOpenmwCfgPath()

    def externalOpenmwCfgExists(self) -> bool:
        """Checks if the external openmw.cfg (user-selected or default location) exists."""
        return Path(self.openmwCfgPath()).is_file()

    def isUsingDefaultPath(self) -> bool:
        """Checks if the plugin is using the default path (no custom path set)."""
        settingValue = self.settings.cfgpath()
        placeholder = "/Path/To/OpenMW/openmw.cfg"
        # Using default if: no value, placeholder value, empty/whitespace, or saved path doesn't exist
        if not settingValue or settingValue == placeholder or not settingValue.strip():
            return True
        # Also using default if saved path no longer exists
        return not Path(settingValue).is_file()

    def settingsCfgPath(self) -> str:
        """Gets the path to settings.cfg (same folder as openmw.cfg)."""
        cfgPath = self.openmwCfgPath()
        return str(Path(cfgPath).parent / "settings.cfg")

    def customLauncherCfgPath(self):
        """Path to the plugin's managed launcher.cfg (profile-local or plugin data)."""
        profile = self._organiser.profile()
        if profile.localSettingsEnabled():
            return str(Path(self.moProfilesPath) / profile.name() / "launcher.cfg")
        return str(Path(self.pluginDataPath) / "launcher.cfg")

    def launcherCfgPath(self) -> str:
        """Gets the path to launcher.cfg (same folder as openmw.cfg)."""
        cfgPath = self.openmwCfgPath()
        return str(Path(cfgPath).parent / "launcher.cfg")

