import mobase, os, glob
from pathlib import Path
from ..core.rootbuilder_plugin import RootBuilderPlugin
from ..modules.rootbuilder_checker import RootBuilderDataChecker
from ..modules.rootbuilder_content import RootBuilderDataContent
from ....common.common_qt import *

class RootBuilderAutobuild(RootBuilderPlugin, mobase.IPluginFileMapper):
    """Autobuild plugin, handles all the automated background parts of Root Builder."""

    def __init__(self):
        super().__init__()
        self._dataChecker = None
        self._dataContent = None

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._organiser.onAboutToRun(lambda appName: self.onAboutToRun(appName))
        self._organiser.onFinishedRun(lambda appName, resultCode: self.onFinishedRun(appName, resultCode))
        self._organiser.onUserInterfaceInitialized(lambda window: self._onUiInit())
        return res

    def _onUiInit(self):
        """Called when UI is initialized - register features that need icons."""
        self._registerDataContent()
        self.migrate()

    def _registerDataContent(self):
        """Register ModDataContent after UI is initialized for proper icon loading."""
        if self._dataContent is not None:
            return  # Already registered

        # Register ModDataChecker to validate Root folders as valid mod content
        self._dataChecker = RootBuilderDataChecker(self._rootBuilder._log)
        self._organiser.gameFeatures().registerFeature(self._organiser.managedGame(), self._dataChecker, priority=100)
        self._rootBuilder._log.debug("Registered Root folder content validator")

        minContentVer = mobase.VersionInfo("2.5.3")
        moVersion = self._organiser.appVersion()
        if moVersion >= minContentVer:
            # Register ModDataContent to show Root Builder content indicator in Content column
            self._dataContent = RootBuilderDataContent(self._rootBuilder._log)
            self._organiser.gameFeatures().registerFeature(self._organiser.managedGame(), self._dataContent, priority=100)
            self._rootBuilder._log.debug("Registered Root folder content indicator")
    
    def master(self):
        return self._pluginName

    def settings(self):
        return []
    
    def name(self):
        return f"{self.baseName()} Autobuild"
    
    def description(self):
        return self.__tr("Handles the automated build and clear for Root Builder's autobuild mode.")
    
    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def migrate(self):
        self._rootBuilder._legacy.migrate()

    def mappings(self):
        """Returns mappings, if there are any, for usvfs mode."""
        return self._rootBuilder.mappings()
    
    def onAboutToRun(self, appName:str) -> bool:
        """Handles automated build, if enabled."""
        # Handle if redirection is needed.
        if self._rootBuilder._settings.redirect():
            self._rootBuilder._log.debug("Redirect enabled, checking for redirection.")
            gamePath = self._rootBuilder._strings.gamePath
            targetsGame = self._rootBuilder._paths.pathShared(glob.escape(gamePath), appName)
            if not targetsGame:
                self._rootBuilder._log.debug("Application is not a game path.")
                modFolders = self._rootBuilder._paths.enabledRootModFolders()
                for mod in modFolders:
                    self._rootBuilder._log.debug(f"Checking for {appName} in {mod}")
                    if self._rootBuilder._paths.pathShared(glob.escape(mod), appName):
                        relativePath = self._rootBuilder._paths.relativePath(mod, appName)
                        self._rootBuilder._log.debug(f"Application found, relative path at {relativePath}")
                        redirectPath = str(Path(gamePath) / relativePath)
                        self._organiser.waitForApplication(self._organiser.startApplication(redirectPath))
                        return False
    
        if self._rootBuilder._settings.autobuild():
            # Handle the automated build now.
            self._rootBuilder.build()

        return True
    
    def onFinishedRun(self, appName:str, resultCode:int):
        """Handles automated clear, if enabled."""
        if self._rootBuilder._settings.autobuild():
            self._rootBuilder.clear()
