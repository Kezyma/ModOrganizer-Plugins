import mobase 
from pathlib import Path
from ..shared.shared_plugin import SharedPlugin
from .openmwplayer import OpenMWPlayer
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class OpenMWPlayerPlugin(SharedPlugin, mobase.IPlugin):

    def __init__(self):
        super().__init__("OpenMWPlayer", "OpenMW Player", mobase.VersionInfo(0, 0, 3, mobase.ReleaseType.ALPHA))

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.openMWPlayer = OpenMWPlayer(self.organiser)
        self.organiser.onAboutToRun(lambda appName: self.runOpenMW(appName))
        return super().init(organiser)

    def name(self):
        return self.baseName()

    def displayName(self):
        return "OpenMW Player"

    def description(self):
        return self.__tr("Launches OpenMW executables using the current mod setup enabled in Mod Organizer 2.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("openmwcfgpath",self.__tr("Path to openmw.cfg"),"/Path/To/OpenMW/openmw.cfg")
            ]
        
    def runOpenMW(self, appName):
        self.openMWPlayer.runOpenMW(appName)