import mobase
from ....base.base_plugin import BasePlugin
from .openmwplayer import OpenMWPlayer
from ....common.common_qt import *

class OpenMWPlayerPlugin(BasePlugin):
    """Base OpenMW Player plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("OpenMWPlayer", "OpenMW Player", mobase.VersionInfo(2, 0, 0, mobase.ReleaseType.FINAL))

    def init(self, organiser:mobase.IOrganizer):
        self._pluginFinder = OpenMWPlayer(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("enabled", self.__tr(f"Enables {self._pluginName}"), True),
            mobase.PluginSetting("openmwcfgpath",self.__tr("Path to openmw.cfg"),"/Path/To/OpenMW/openmw.cfg"),
            mobase.PluginSetting("dummyesp",self.__tr("Enables omwaddon and omwscripts support via esp files."), False)
            ]
        for setting in customSettings:
            baseSettings.append(setting)
        return customSettings