import mobase, threading
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
        self._organiser = organiser
        organiser.onAboutToRun(lambda appName: self.runOpenMW(appName))
        #organiser.onFinishedRun(lambda appName, resultCode: self.importChanges(appName, resultCode))
        organiser.onUserInterfaceInitialized(lambda window: self.onUserInterfaceInitialized())
        organiser.onProfileChanged(lambda old, new: self.onProfileChanged)
        organiser.modList().onModInstalled(lambda mod: self.onModInstalled(mod))
        organiser.modList().onModStateChanged(lambda mods: self.onModStateChanged())
        organiser.modList().onModMoved(lambda mod, old, new: self.refreshConfig())
        organiser.modList().onModRemoved(lambda name: self.refreshConfig())
        organiser.pluginList().onPluginMoved(lambda name, old, new: self.refreshConfig())
        organiser.pluginList().onPluginStateChanged(lambda plugin, map: self.refreshConfig())
        return super().init(organiser)
        
    def name(self):
        return self.baseName()

    def description(self):
        return self.__tr("Launches OpenMW executables using the current mod setup enabled in Mod Organizer 2.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
        
    def runOpenMW(self, appName):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            return self.openMWPlayer.newRunOpenMw(appName)

    def importChanges(self, appName, resultCode):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.openMWPlayer.newImportOpenMwCfg()
            self.openMWPlayer.newImportSettingsCfg()

    def onUserInterfaceInitialized(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.openMWPlayer.newInitialSetup()
            self.createDummyBulk()
            self.refreshConfig()

    def onModInstalled(self, mod):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.createDummy(mod)
            self.refreshConfig()

    def onModStateChanged(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.createDummyBulk()
            self.refreshConfig()

    def onProfileChanged(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.openMWPlayer.newInitialSetup()
            self.refreshConfig()

    def onRefreshed(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.openMWPlayer.newInitialSetup()
            self.refreshConfig()

    def createDummy(self, mod):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            if self.openMWPlayer.settings.dummyesp():
                modChanged = self.openMWPlayer.createDummy(mod.name())
                if modChanged == True:
                    self.organiser.refresh()

    def createDummyBulk(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            if self.openMWPlayer.settings.dummyesp():
                self.openMWPlayer.enableDummy()

    _refreshing = False
    def refreshConfig(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            if (self._refreshing == False):
                self._refreshing = True
                qInfo("Refreshing openmw.cfg & settings.cfg")
                t = threading.Thread(target=self.refreshConfigAsync, daemon=True)
                t.start()

    def refreshConfigAsync(self):
        self.openMWPlayer.newRefreshContentAndData()
        self._refreshing = False