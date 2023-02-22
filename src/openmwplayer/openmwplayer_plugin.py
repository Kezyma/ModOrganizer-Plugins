import mobase 
from pathlib import Path
from ..shared.shared_plugin import SharedPlugin
from .openmwplayer import OpenMWPlayer
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class OpenMWPlayerPlugin(SharedPlugin):

    def __init__(self):
        super().__init__("OpenMWPlayer", "OpenMW Player", mobase.VersionInfo(0, 0, 13, mobase.ReleaseType.ALPHA))

    def init(self, organiser=mobase.IOrganizer):
        self.openMWPlayer = OpenMWPlayer(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("openmwcfgpath",self.__tr("Path to openmw.cfg"),"/Path/To/OpenMW/openmw.cfg"),
            mobase.PluginSetting("dummyesp",self.__tr("Enables omwaddon and omwscripts support via esp files."), False),
            mobase.PluginSetting("managesettings",self.__tr("Manage openmw.cfg settings through Mod Organizer."), False)
            ]