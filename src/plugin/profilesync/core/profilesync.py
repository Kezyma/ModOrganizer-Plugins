import mobase
from ....common.common_log import CommonLog
from .profilesync_settings import ProfileSyncSettings
from ..modules.profilesync_groups import ProfileSyncGroups
from ..modules.profilesync_strings import ProfileSyncStrings
from ..modules.profilesync_sync import ProfileSyncSync
from ..modules.profilesync_legacy import ProfileSyncLegacy

class ProfileSync:
    """Core Profile Sync class that handles all plugin functionality."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = ProfileSyncSettings(self._organiser)
        self._log = CommonLog("ProfileSync", self._settings)
        self._strings = ProfileSyncStrings("ProfileSync", self._organiser)
        self._groups = ProfileSyncGroups(self._organiser, self._strings, self._log)
        self._sync = ProfileSyncSync(self._organiser, self._strings, self._groups, self._log)
        self._legacy = ProfileSyncLegacy(self._organiser, self._strings, self._settings, self._groups, self._log)

    