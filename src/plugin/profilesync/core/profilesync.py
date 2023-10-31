import mobase
from pathlib import Path
from ....common.common_log import CommonLog
from ....common.common_utilities import CommonUtilities
from .profilesync_settings import ProfileSyncSettings

class ProfileSync():
    """Core Profile Sync class that handles all plugin functionality."""

    def __init__(self, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._settings = ProfileSyncSettings(self._organiser)
        self._log = CommonLog("ProfileSync", self._organiser, self._settings)
        self._util = CommonUtilities(self._organiser)
        super().__init__()