import mobase, glob, threading, subprocess
from pathlib import Path
from ....common.common_log import CommonLog
from ....common.common_paths import CommonPaths
from ....common.common_utilities import *
from .openmwplayer_settings import OpenMWPlayerSettings
from ..modules.openmwplayer_strings import OpenMWPlayerStrings
from ..modules.openmwplayer_files import OpenMWPlayerFiles
from ..modules.openmwplayer_import import OpenMWPlayerImport
from ..modules.openmwplayer_deploy import OpenMWPlayerDeploy
from ..modules.openmwplayer_mappings import OpenMWPlayerMappings

class OpenMWPlayer:
    """Core OpenMW Player class."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = OpenMWPlayerSettings(self._organiser)
        self._log = CommonLog("OpenMWPlayer", self._settings)
        self._paths = CommonPaths("OpenMWPlayer", self._organiser)
        self._strings = OpenMWPlayerStrings("OpenMWPlayer", self._organiser, self._settings)
        self._files = OpenMWPlayerFiles(self._organiser, self._settings, self._strings, self._log)
        self._import = OpenMWPlayerImport(self._organiser, self._settings, self._strings)
        self._deploy = OpenMWPlayerDeploy(self._organiser, self._settings, self._strings)
        self._mappings = OpenMWPlayerMappings(self._organiser, self._settings, self._strings, self._log)
        # Thread-safety: flag and lock for deferred MO2 refresh
        self._pendingRefresh = False
        self._refreshLock = threading.Lock()
        # Redirect detection for startApplication loop prevention
        self._inRedirect = False
        self._redirectPath = None

    def initialSetup(self):
        """Imports any missing openmw.cfg, settings.cfg, or launcher.cfg for OpenMW Player to use."""
        if not Path(self._strings.pluginDataPath).exists():
            os.makedirs(self._strings.pluginDataPath, exist_ok=True)
        if not Path(self._strings.customOpenmwCfgPath()).exists():
            self._import.importOpenmwCfg()
        if not Path(self._strings.customSettingsCfgPath()).exists():
            self._import.importSettingsCfg()
        if not Path(self._strings.customLauncherCfgPath()).exists():
            self._import.importLauncherCfg()
        self._files.refreshOpenmwCfg()
        self.setupDummyEsps()

    def importSettings(self):
        """Imports and overwrites the current openmw.cfg, settings.cfg, and launcher.cfg."""
        self._import.importOpenmwCfg()
        self._import.importSettingsCfg()
        self._import.importLauncherCfg()
        self._files.refreshOpenmwCfg()

    def toggleDummyEsps(self, enabled:bool):
        self._settings.updateSetting("dummyesp", enabled)
        self.setupDummyEsps()

    def setupDummyEspsAsync(self):
        """Run setupDummyEsps in background thread. Use checkPendingRefresh() afterwards on main thread."""
        nt = threading.Thread(target=self._setupDummyEspsBackground, daemon=True)
        nt.start()

    def _setupDummyEspsBackground(self):
        """Background-safe version that sets flag instead of calling refresh directly."""
        needsRefresh = self._setupDummyEspsInternal()
        if needsRefresh:
            with self._refreshLock:
                self._pendingRefresh = True

    def setupDummyEsps(self):
        """Sets up dummy ESPs and refreshes MO2 if needed. MUST be called from main thread."""
        needsRefresh = self._setupDummyEspsInternal()
        if needsRefresh:
            self._organiser.refresh()

    def _setupDummyEspsInternal(self):
        """Internal method that creates/deletes dummy ESPs. Thread-safe, does not call refresh."""
        if self._settings.dummyesp():
            return self.createDummyEsps()
        else:
            return self.deleteDummyEsps()

    def checkPendingRefresh(self):
        """Check if refresh is pending and perform it. MUST be called from main thread."""
        with self._refreshLock:
            if self._pendingRefresh:
                self._pendingRefresh = False
                self._organiser.refresh()
        
    def createDummyEsps(self):
        refresh = False
        dataPaths = [
            self._strings.gameDataFolder,
            f"{self._strings.moModsPath}\\*",
            self._strings.moOverwritePath
        ]
        dummyEspSource = str(Path(__file__).parent.parent / "data" / "openmwplayer_dummy.esp")
        self._log.debug("Creating dummy esp files.")
        for path in dataPaths:
            globAddon = f"{path}\\*.omwaddon"
            globScript = f"{path}\\*.omwscripts"
            self._log.debug(f"Searching {globAddon}")
            for match in glob.glob(globAddon):
                self._log.debug(f"Found {match}")
                dummyPath = Path(f"{match}.esp")
                if not dummyPath.exists():
                    copyFile(dummyEspSource, str(dummyPath))
                    refresh = True
            self._log.debug(f"Searching {globScript}")
            for match in glob.glob(globScript):
                self._log.debug(f"Found {match}")
                dummyPath = Path(f"{match}.esp")
                if not dummyPath.exists():
                    copyFile(dummyEspSource, str(dummyPath))
                    refresh = True
        return refresh
    
    def deleteDummyEsps(self):
        refresh = False
        dataPaths = [
            self._strings.gameDataFolder,
            f"{self._strings.moModsPath}\\*",
            self._strings.moOverwritePath
        ]
        for path in dataPaths:
            globAddon = f"{path}\\*.omwaddon.esp"
            globScript = f"{path}\\*.omwscripts.esp"
            for match in glob.glob(globAddon):
                deleteFile(match)
                refresh = True
            for match in glob.glob(globScript):
                deleteFile(match)
                refresh = True
        return refresh

    def runApplication(self, appName) -> bool:
        """Handle application launch based on mode."""
        appPath = str(appName)
        fileName = os.path.basename(appPath).lower()

        # Auto-record OpenMW executable path
        if fileName == "openmw.exe" or fileName.startswith("openmw-"):
            self._settings.updateSetting("openmwexepath", appPath)
            self._log.info(f"Recorded OpenMW path: {appPath}")

        # Check if this is our redirect callback (prevents infinite loop)
        if self._inRedirect and appPath == self._redirectPath:
            self._log.debug("Detected redirect callback, allowing through")
            self._inRedirect = False
            self._redirectPath = None
            return True  # Let MO2 run with USVFS mappings

        # Refresh config before any launch
        self._files.refreshOpenmwCfg()

        # Legacy mode: use existing behavior
        if self._settings.legacymode():
            return self._runApplicationLegacy(appPath, fileName)

        # USVFS mode
        return self._runApplicationUsvfs(appPath, fileName)

    def _runApplicationLegacy(self, appPath: str, fileName: str) -> bool:
        """Legacy mode: existing subprocess/deploy behavior."""
        if fileName in [x.lower() for x in self._strings.openMWSupportedExecutables]:
            # This is the OpenMW.exe, can be launched with parameters.
            profile = self._organiser.profile()
            customCfgPath = str(Path(self._strings.customOpenmwCfgPath()).parent)
            args = [appPath, "--replace", "config", "--config", f"\"{customCfgPath}\""]
            if profile.localSavesEnabled():
                localSavePath = self._strings.localSavesPath()
                args.extend(["--replace", "user-data", "--user-data", f"\"{localSavePath}\""])
            subprocess.call(args)
            return False
        else:
            # This is some other executable, deploy files.
            self._deploy.deployCfg()
            return True

    def _runApplicationUsvfs(self, appPath: str, fileName: str) -> bool:
        """USVFS mode: run through MO2 with mappings."""
        profile = self._organiser.profile()

        # For openmw.exe with profile saves, we need --user-data argument
        # This requires using startApplication to pass arguments
        if fileName in [x.lower() for x in self._strings.openMWSupportedExecutables]:
            if profile.localSavesEnabled():
                # Need to pass --user-data argument
                localSavePath = self._strings.localSavesPath()

                # Ensure saves directory exists
                savesPath = Path(localSavePath) / "saves"
                if not savesPath.exists():
                    os.makedirs(savesPath, exist_ok=True)

                args = [f'--replace', 'user-data', '--user-data', f'"{localSavePath}"']

                self._log.debug(f"Launching {appPath} with args: {args}")

                # Set redirect detection flags BEFORE calling startApplication
                self._inRedirect = True
                self._redirectPath = appPath
                basePath = Path(appPath).parent

                # Launch through MO2 with arguments
                handle = self._organiser.startApplication(appPath, args, basePath)
                self._organiser.waitForApplication(handle)

                return False  # We handled the launch
            else:
                # No profile saves - config mappings via USVFS are sufficient
                self._log.debug("Launching openmw.exe through MO2 (USVFS mode, no profile saves)")
                return True  # Let MO2 handle with USVFS mappings

        # For other executables, just let MO2 run with USVFS mappings
        self._log.debug(f"Launching {fileName} through MO2 (USVFS mode)")
        return True