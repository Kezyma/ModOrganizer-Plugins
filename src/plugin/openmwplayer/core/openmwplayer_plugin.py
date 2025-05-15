import mobase
from pathlib import Path
from ....base.base_plugin import BasePlugin
from .openmwplayer import OpenMWPlayer
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ....common.common_qt import *

class OpenMWPlayerPlugin(BasePlugin):
    """Base OpenMW Player plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("OpenMWPlayer", "OpenMW Player", mobase.VersionInfo(2, 0, 2))

    def init(self, organiser:mobase.IOrganizer):
        self._openmwPlayer = OpenMWPlayer(organiser)
        self._update = CommonUpdate(
            "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/openmwplayer.json", 
            "https://www.nexusmods.com/morrowind/mods/52345?tab=files", 
            self, self._openmwPlayer._strings, self._openmwPlayer._log)
        self._help = CommonHelp(Path(__file__).parent.parent / "data" / "openmwplayer_help.html", 
                                "openmwplayer", "morrowind", "52345", 
                                self._openmwPlayer._strings, self._openmwPlayer._log)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("openmwcfgpath",self.__tr("Path to openmw.cfg"),"/Path/To/OpenMW/openmw.cfg"),
            mobase.PluginSetting("dummyesp",self.__tr("Enables omwaddon and omwscripts support via esp files."), False)
            ]
        for setting in customSettings:
            baseSettings.append(setting)
        return baseSettings
