import mobase, threading
from ..core.openmwplayer_plugin import OpenMWPlayerPlugin
from ..modules.openmwplayer_menu import OpenMWPlayerMenu
from ..modules.openmwplayer_checker import OpenMWPlayerDataChecker
from ..modules.openmwplayer_content import OpenMWPlayerDataContent
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *

try:
    from PyQt5.QtCore import QTimer
except ImportError:
    from PyQt6.QtCore import QTimer

class OpenMWPlayerLauncher(OpenMWPlayerPlugin, mobase.IPlugin):
    def __init__(self):
        super().__init__()
        self._dataChecker = None
        self._dataContent = None

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._organiser.onUserInterfaceInitialized(lambda window: self._onUiInit())
        return res

    def _onUiInit(self):
        """Called when UI is initialized - game is now loaded."""
        managedGame = self._organiser.managedGame()
        if managedGame is None:
            return
        
        gameName = managedGame.gameName().lower()
        if "morrowind" in gameName or "openmw" in gameName:
            self._organiser.onAboutToRun(lambda appName: self.onApplicationLaunch(appName))
            self._organiser.onFinishedRun(lambda appName, exitCode: self.onApplicationClose(appName))
            self._organiser.onProfileChanged(lambda old, new: self.onModListChange())

            modList:mobase.IModList = self._organiser.modList()
            modList.onModInstalled(lambda mod: self.onModListChange())
            modList.onModStateChanged(lambda mods: self.onModListChange())
            modList.onModMoved(lambda mod, old, new: self.onModListChange())
            modList.onModRemoved(lambda name: self.onModListChange())

            pluginList:mobase.IPluginList = self._organiser.pluginList()
            pluginList.onPluginMoved(lambda name, old, new: self.onModListChange())
            pluginList.onPluginStateChanged(lambda map: self.onModListChange())

            self._registerGameFeatures()
            self.onModListChange()

    def _registerGameFeatures(self):
        """Register ModDataChecker and ModDataContent after game is loaded."""
        if self._dataChecker is not None:
            return  # Already registered

        managedGame = self._organiser.managedGame()
        if managedGame is None:
            return

        gameName = managedGame.gameName().lower()
        if "morrowind" in gameName or "openmw" in gameName:
            # Register ModDataChecker to validate OpenMW files as valid content
            self._dataChecker = OpenMWPlayerDataChecker(self._openmwPlayer._log)
            self._organiser.gameFeatures().registerFeature(self._dataChecker, priority=100)

            minContentVer = mobase.VersionInfo("2.5.3")
            moVersion = self._organiser.appVersion()
            if moVersion >= minContentVer:
                # Register ModDataContent to show OpenMW content indicator in Content column
                self._dataContent = OpenMWPlayerDataContent(self._openmwPlayer._log)
                self._organiser.gameFeatures().registerFeature(self._dataContent, priority=100)

            self._openmwPlayer._log.debug("Registered OpenMW content validator and indicator")

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return OPENMW_ICON

    def master(self):
        return self.baseName()

    def name(self):
        return self.baseName() + " Launcher"

    def displayName(self):
        return self.baseDisplayName() + " Launcher"

    def description(self):
        return self.__tr("Handles background running of OpenMW Player jobs.")

    def settings(self):
        return []

    def onModListChange(self):
        """Handle mod list changes - pre-fetch MO2 data on main thread, then spawn background threads."""
        # CRITICAL: Pre-fetch all MO2 API data on main thread BEFORE spawning any threads
        # MO2's API is NOT thread-safe and calling it from background threads causes deadlocks
        dataFolders = self._openmwPlayer._files.getDataFolders()
        enabledPlugins = self._openmwPlayer._files.getEnabledPlugins()

        # Spawn background threads with pre-fetched data (thread-safe operations only)
        t1 = threading.Thread(
            target=self._openmwPlayer._files._refreshOpenmwCfgWithData,
            args=(dataFolders, enabledPlugins),
            daemon=True
        )
        t2 = threading.Thread(
            target=self._openmwPlayer._setupDummyEspsBackground,
            daemon=True
        )
        t1.start()
        t2.start()

        # Schedule a check for pending refresh on main thread after background work likely completes
        # Using QTimer.singleShot ensures the callback runs on the main thread
        QTimer.singleShot(500, self._checkPendingRefresh)

    def _checkPendingRefresh(self):
        """Check if background operations flagged a need for MO2 refresh. Runs on main thread."""
        self._openmwPlayer.checkPendingRefresh()

    def onApplicationLaunch(self, appName):
        return self._openmwPlayer.runApplication(appName)

    def onApplicationClose(self, appName):
        self._openmwPlayer._deploy.restoreCfg()
