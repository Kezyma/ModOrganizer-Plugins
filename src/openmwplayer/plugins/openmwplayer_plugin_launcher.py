import mobase 
from pathlib import Path
from ..openmwplayer_plugin import OpenMWPlayerPlugin
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class OpenMWPlayerPluginLauncher(OpenMWPlayerPlugin, mobase.IPlugin):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        organiser.onAboutToRun(lambda appName: self.runOpenMW(appName))
        organiser.onModInstalled(lambda mod: self.createDummy(mod))
        return super().init(organiser)
        
    def name(self):
        return self.baseName()

    def description(self):
        return self.__tr("Launches OpenMW executables using the current mod setup enabled in Mod Organizer 2.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
        
    def runOpenMW(self, appName):
        return self.openMWPlayer.runOpenMW(appName)

    def createDummy(self, mod):
        if self.openMWPlayer.settings.dummyesp():
            self.openMWPlayer.createDummy(mod)
