    
import mobase

try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

from ..moddy_plugin import ModdyPlugin

class ModdyCheckerPlugin(ModdyPlugin, mobase.IPlugin):
    """ Main Moddy plugin. Handles popup alerts. """

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.organiser.onAboutToRun(lambda appName: self.runChecks(appName))
        self.organiser.onUserInterfaceInitialized(lambda window: self.firstRun())
        
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    def description(self):
        return self.__tr("Monitors Mod Organizer for potential issues and warns the user of them.")

    def runChecks(self, appName):
        """ Check for errors and display warnings. """
        return self.moddy.run()
    
    def firstRun(self):
        self.moddy.firstRun()
    
    