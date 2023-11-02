import mobase, threading
from pathlib import Path
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
        group = self._groups.groupFromProfile(profile)
        if group is not None:
            profilePath = self._strings.moProfilePath()
            modListPath = Path(profilePath) / "modlist.txt"
            modLines = self._util.loadLines(str(modListPath))
            modOrder = []
            for line in modLines:
                if line.startswith("+") or line.startswith("-"):
                    modOrder.append(line.replace("+", "").replace("-", ""))

            groupListPath = self._groups.groupModlist(group)
            self._util.saveLines(groupListPath, modOrder)


    _modList = []
    def syncFromGroup(self, group:str):
        """Syncs all profiles in a selected group."""
        groups = self._groups.loadSyncGroups()
        groupList = groups[group]
        modListPath = self._groups.groupModlist(group)
        self._modList = self._util.loadLines(modListPath)
        tasks = []
        for profile in groupList:
            nt = threading.Thread(target=self._syncToProfile, args=[profile])
            nt.start()
            tasks.append(nt)
        for t in tasks:
            t.join()

    def _syncToProfile(self, profile:str):
        profilesPath = Path(self._strings.moProfilesPath())
        modListPath = profilesPath / profile / "modlist.txt"
        modList = self._util.loadLines(str(modListPath))
        newList = []
        for modName in self._modList:
            enabledName = "+" + modName
            if enabledName in modList:
                newList.append(enabledName)
            else:
                newList.append("-" + modName)
        self._util.saveLines(str(modListPath), newList)
