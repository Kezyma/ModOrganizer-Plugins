import mobase 
from ..shared.shared_plugin import SharedPlugin
from .creationeer import Creationeer
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class CreationeerPlugin(SharedPlugin):

    def __init__(self):
        super().__init__("Creationeer", "Creationeer", mobase.VersionInfo(0,0,1, mobase.ReleaseType.ALPHA))

    def init(self, organiser=mobase.IOrganizer):
        self.creationeer = Creationeer(organiser)
        res = super().init(organiser)
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("enabled","Enables Creationeer",True),
            mobase.PluginSetting("rootbuildersupport","Enables support for Root Builder.", False),
            mobase.PluginSetting("modnameformat","Format for mod names.", "Creation Club - {creation}")
            ]