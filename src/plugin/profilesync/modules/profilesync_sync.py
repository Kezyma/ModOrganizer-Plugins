import mobase, threading
from pathlib import Path
from .profilesync_groups import ProfileSyncGroups
from .profilesync_strings import ProfileSyncStrings
from ....common.common_utilities import saveLines, loadLines
from ....common.common_log import CommonLog

class ProfileSyncSync:
    """Profile Sync Sync module, handles updating profile modlists."""

    def __init__(self, organiser: mobase.IOrganizer, strings: ProfileSyncStrings, groups: ProfileSyncGroups, log: CommonLog) -> None:
        self._organiser = organiser
        self._strings = strings
        self._log = log
        self._groups = groups

    def syncFromCurrentProfile(self):
        profile = self._organiser.profile()
        group = self._groups.groupFromProfile(profile.name())
        if group is not None:
            mods = self._organiser.modList().allModsByProfilePriority(profile)
            mods.reverse()
            modList = []
            enabledStates = []
            for m in mods:
                modList.append(f"{m}\n")
                if self._organiser.modList().state(m) & mobase.ModState.ACTIVE:
                    enabledStates.append(f"+{m}\n")
                else:
                    enabledStates.append(f"-{m}\n")
            groupListPath = self._groups.groupModlist(group)
            saveLines(groupListPath, modList)

            stateGroups = self._groups.stateGroupsForProfile(profile.name())
            for stateGroup in stateGroups:
                listPath = self._groups.stateGroupModlist(group, stateGroup)
                saveLines(listPath, enabledStates)

    def syncFromProfile(self, profile:str):
        """Syncs a group to a selected profile."""
        group = self._groups.groupFromProfile(profile)
        if group is not None:
            self._log.debug(f"Sync from {profile} to group {group}")
            profilePath = self._strings.moProfilePath
            modListPath = Path(profilePath) / "modlist.txt"
            self._log.debug(f"Loading modlist {modListPath}")
            modLines = loadLines(str(modListPath))
            rawLines = []
            modOrder = []
            for line in modLines:
                if line.startswith("+") or line.startswith("-"):
                    modOrder.append(f"{line[1:]}\n")
                rawLines.append(f"{line}\n")
            groupListPath = self._groups.groupModlist(group)
            self._log.debug(f"Saving group list {groupListPath}")
            saveLines(groupListPath, modOrder)

            stateGroups = self._groups.stateGroupsForProfile(profile)
            for stateGroup in stateGroups:
                listPath = self._groups.stateGroupModlist(group, stateGroup)
                saveLines(listPath, rawLines)

    _modList = []
    _stateGroups = {}
    _stateModlists = {}
    def syncFromGroup(self, group:str):
        """Syncs all profiles in a selected group."""
        groups = self._groups.loadSyncGroups()
        groupList = groups[group][self._groups.PROFILES]
        modListPath = self._groups.groupModlist(group)
        self._modList = loadLines(modListPath)

        self._stateGroups = groups[group][self._groups.STATEGROUPS]
        self._stateModlists = {}
        for sg in self._stateGroups:
            statePath = self._groups.stateGroupModlist(group, sg)
            if Path(statePath).exists():
                self._stateModlists[sg] = self.modlistToCategories(loadLines(statePath))
        
        tasks = []
        for profile in groupList:
            self._log.debug(f"Sync from group {group} to {profile}")
            nt = threading.Thread(target=self._syncToProfile, args=[profile])
            nt.start()
            tasks.append(nt)
        for t in tasks:
            t.join()

    def _syncToProfile(self, profile:str):
        profilesPath = Path(self._strings.moProfilesPath)
        modListPath = profilesPath / profile / "modlist.txt"
        modList = loadLines(str(modListPath))
        newList = []

        stateMods = []
        stateGroups = self._groups.stateGroupsForProfile(profile)
        for g in stateGroups:
            groupInfo = self._stateGroups[g]
            groupList = self._stateModlists[g]
            syncCats = groupInfo[self._groups.CATEGORIES]
            for cat in syncCats:
                catLabel = f"-{cat}"
                if catLabel in groupList:
                    stateMods.extend(groupList[catLabel])

        for modName in self._modList:
            enabledName = f"+{modName}"
            disabledName = f"-{modName}"
            if enabledName in stateMods:
                newList.append(f"{enabledName}\n")
            elif disabledName in stateMods:
                newList.append(f"{disabledName}\n")
            else:
                if enabledName in modList:
                    newList.append(f"{enabledName}\n")
                else:
                    newList.append(f"-{modName}\n")
        self._log.debug(f"Saving modlist {modListPath}")
        saveLines(str(modListPath), newList)

    def modlistToCategories(self, modList:list) -> dict:
        modList.reverse()
        cats = {}
        currentCat = None
        for mod in modList:
            modStr = str(mod)
            if modStr.endswith("_separator"):
                currentCat = modStr.replace("_separator","")
                cats[currentCat] = []
            elif currentCat is not None:
                cats[currentCat].append(mod)
        return cats