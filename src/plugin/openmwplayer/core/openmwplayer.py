import mobase
from ....common.common_log import CommonLog
from ....common.common_paths import CommonPaths
from .openmwplayer_settings import OpenMWPlayerSettings
from ..modules.openmwplayer_strings import OpenMWPlayerStrings

class OpenMWPlayer:
    """Core OpenMW Player class."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = OpenMWPlayerSettings(self._organiser)
        self._log = CommonLog("OpenMWPlayer", self._settings)
        self._paths = CommonPaths("OpenMWPlayer", self._organiser)
        self._strings = OpenMWPlayerStrings("OpenMWPlayer", self._organiser, self._settings)