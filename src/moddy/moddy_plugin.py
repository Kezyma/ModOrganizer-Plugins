import mobase 
from ..shared.shared_plugin import SharedPlugin
from .moddy import Moddy
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class ModdyPlugin(SharedPlugin):

    def __init__(self):
        super().__init__("Moddy", "Moddy", mobase.VersionInfo(0, 0, 1, mobase.ReleaseType.ALPHA))

    def init(self, organiser=mobase.IOrganizer):
        self.moddy = Moddy(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("enabled",self.__tr("Enables Moddy"),True),            
            mobase.PluginSetting("disabledchecks",self.__tr("List of checks that should be skipped."), ""),
            mobase.PluginSetting("messagelevel",self.__tr("Threshold for displaying messages."), 4),
            mobase.PluginSetting("notificationsonly",self.__tr("If enabled, Moddy will not pop up and only notifications will be shown."), False),
            ]
