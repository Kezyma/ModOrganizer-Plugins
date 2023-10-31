import mobase
from .profilesync_groups import ProfileSyncGroups
from .profilesync_strings import ProfileSyncStrings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog

class ProfileSyncSync():
    """Profile Sync Sync module, handles updating profile modlists."""

    def __init__(self, organiser:mobase.IOrganizer,strings:ProfileSyncStrings,groups:ProfileSyncGroups,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._util = utilities
        self._log = log
        self._groups = groups

    def syncFromProfile(self, profile:str):
        """Syncs a group to a selected profile."""

    def syncFromGroup(self, group:str):
        """Syncs all profiles in a selected group."""