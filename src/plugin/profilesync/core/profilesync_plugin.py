import mobase
from pathlib import Path
from ....base.base_plugin import BasePlugin
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ....common.common_qt import *
from .profilesync import ProfileSync

class ProfileSyncPlugin(BasePlugin):
    """Base Profile Sync plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("ProfileSync", "Profile Sync", mobase.VersionInfo(2, 0, 1))

    def init(self, organiser:mobase.IOrganizer):
        self._profileSync = ProfileSync(organiser)
        self._update = CommonUpdate(
            "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/profilesync.json", 
            "https://www.nexusmods.com/skyrimspecialedition/mods/60690?tab=files", 
            self, self._profileSync._strings, self._profileSync._log)
        self._help = CommonHelp(Path(__file__).parent.parent / "data" / "profilesync_help.html",
                                "profilesync", "skyrimspecialedition", "60690",
                                self._profileSync._strings, self._profileSync._log)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = []
        for setting in customSettings:
            baseSettings.append(setting)
        return baseSettings
        