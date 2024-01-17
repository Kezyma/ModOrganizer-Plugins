import mobase, glob, threading
from pathlib import Path
from ....common.common_log import CommonLog
from ....common.common_paths import CommonPaths
from ....common.common_utilities import *
from .openmwplayer_settings import OpenMWPlayerSettings
from ..modules.openmwplayer_strings import OpenMWPlayerStrings
from ..modules.openmwplayer_files import OpenMWPlayerFiles
from ..modules.openmwplayer_import import OpenMWPlayerImport

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

    def initialSetup(self):
        """Imports any missing openmw.cfg or settings.cfg for OpenMW Player to use."""
        profile = self._organiser.profile().name()
        if not Path(self._strings.customOpenmwCfgPath(profile)).exists():
            self._import.importOpenmwCfg(profile)
        if not Path(self._strings.customSettingsCfgPath(profile)).exists():
            self._import.importSettingsCfg(profile)
        self._files.refreshOpenmwCfg()
        self.setupDummyEsps()

    def importSettings(self):
        """Imports and overwrites the current openmw.cfg and settings.cfg."""
        self._import.importOpenmwCfg()
        self._import.importSettingsCfg()
        self._files.refreshOpenmwCfg()

    def toggleDummyEsps(self, enabled:bool):
        self._settings.updateSetting("dummyesp", enabled)
        self.setupDummyEsps()

    def setupDummyEsps(self):
        if self._settings.dummyesp():
            nt = threading.Thread(target=self.createDummyEsps)
            nt.start()
        else:
            nt = threading.Thread(target=self.deleteDummyEsps)
            nt.start()

    def createDummyEsps(self):
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
            self._log.debug(f"Searching {globScript}")
            for match in glob.glob(globScript):
                self._log.debug(f"Found {match}")
                dummyPath = Path(f"{match}.esp")
                if not dummyPath.exists():
                    copyFile(dummyEspSource, str(dummyPath))
        self._organiser.refresh()
    
    def deleteDummyEsps(self):
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
            for match in glob.glob(globScript):
                deleteFile(match)
        self._organiser.refresh()
