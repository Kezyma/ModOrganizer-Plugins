import mobase
from ....base.base_plugin import BasePlugin
from .profilesync import ProfileSync
from ....common.common_qt import *

class ProfileSyncPlugin(BasePlugin):
    """Base Profile Sync plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("ProfileSync", "Profile Sync", mobase.VersionInfo(2, 0, 0, mobase.ReleaseType.FINAL))

    def init(self, organiser:mobase.IOrganizer):
        self._profileSync = ProfileSync(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("enabled",self.__tr(f"Enables {self._pluginName}"), True)
            ]
        for setting in customSettings:
            baseSettings.append(setting)
        return customSettings
        