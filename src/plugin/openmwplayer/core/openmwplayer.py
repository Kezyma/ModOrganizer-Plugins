import mobase
from pathlib import Path
from ....common.common_log import CommonLog
from ....common.common_paths import CommonPaths
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

    def importSettings(self):
        """Imports and overwrites the current openmw.cfg and settings.cfg."""
        self._import.importOpenmwCfg()
        self._import.importSettingsCfg()
        self._files.refreshOpenmwCfg()

    def toggleDummyEsp(self, enabled:bool):
        pass
