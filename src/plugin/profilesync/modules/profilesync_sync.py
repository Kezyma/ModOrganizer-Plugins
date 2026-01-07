import mobase, threading
from pathlib import Path
from typing import Dict, List
from .profilesync_groups import ProfileSyncGroups
from .profilesync_strings import ProfileSyncStrings
from ..core.profilesync_settings import ProfileSyncSettings
from ....common.common_utilities import saveLines, loadLines
from ....common.common_log import CommonLog
from ..models.profilesync_groupdata import *

class ProfileSyncSync:
    """Profile Sync Sync module, handles updating profile modlists."""

    def __init__(self, organiser: mobase.IOrganizer, strings: ProfileSyncStrings, groups: ProfileSyncGroups, log: CommonLog, settings: ProfileSyncSettings) -> None:
        self._organiser = organiser
        self._strings = strings
        self._log = log
        self._groups = groups
        self._settings = settings
        self._syncLock = threading.Lock()

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
            if saveLines(groupListPath, modList):
                self._log.debug(f"Saved {groupListPath}")
            else:
                self._log.info(f"Could not save {groupListPath}")

            stateGroups = self._groups.stateGroupsForProfile(profile.name())
            for stateGroup in stateGroups:
                listPath = self._groups.stateGroupModlist(group, stateGroup)
                if saveLines(listPath, enabledStates):
                    self._log.debug(f"Saved {listPath}")
                else:
                    self._log.info(f"Could not save {listPath}")

    def syncFromProfile(self, profile:str):
        """Syncs a group to a selected profile."""
        group = self._groups.groupFromProfile(profile)
        if group is not None:
            self._log.debug(f"Sync from {profile} to group {group}")
            profilePath = self._strings.moProfilePath
            modListPath = Path(profilePath) / "modlist.txt"
            self._log.debug(f"Loading modlist {modListPath}")
            modLines = loadLines(str(modListPath))
            if modLines is None:
                self._log.warning(f"Could not read modlist {modListPath}")
                return
            rawLines = []
            modOrder = []
            for line in modLines:
                if line.startswith("+") or line.startswith("-"):
                    modOrder.append(f"{line[1:]}\n")
                rawLines.append(f"{line}\n")
            groupListPath = self._groups.groupModlist(group)
            self._log.debug(f"Saving group list {groupListPath}")
            if saveLines(groupListPath, modOrder):
                self._log.debug(f"Saved {groupListPath}")
            else:
                self._log.info(f"Could not save {groupListPath}")

            stateGroups = self._groups.stateGroupsForProfile(profile)
            for stateGroup in stateGroups:
                listPath = self._groups.stateGroupModlist(group, stateGroup)
                if saveLines(listPath, rawLines):
                    self._log.debug(f"Saved {listPath}")
                else:
                    self._log.info(f"Could not save {listPath}")

    def syncFromGroup(self, group:str):
        """Syncs all profiles in a selected group."""
        tasks = []
        with self._syncLock:
            groups = self._groups.loadSyncGroups()
            groupList = groups[group][PROFILES]
            modListPath = self._groups.groupModlist(group)
            modList = loadLines(modListPath)

            if modList is None:
                self._log.warning(f"Could not read group modlist {modListPath}")
                return

            stateGroups = groups[group][STATEGROUPS]
            stateModlists = {}
            for sg in stateGroups:
                statePath = self._groups.stateGroupModlist(group, sg)
                if Path(statePath).exists():
                    stateLines = loadLines(statePath)
                    if stateLines is not None:
                        stateModlists[sg] = self.modlistToCategories(stateLines)
                    else:
                        self._log.warning(f"Could not read state group modlist {statePath}")

            for profile in groupList:
                self._log.debug(f"Sync from group {group} to {profile}")
                if self._settings.useasync():
                    nt = threading.Thread(target=self._syncToProfileSafe, args=[profile, modList, stateGroups, stateModlists])
                    nt.start()
                    tasks.append(nt)
                else:
                    self._syncToProfile(profile, modList, stateGroups, stateModlists)
        # Lock released - now safe to wait for threads without risk of deadlock
        if self._settings.useasync():
            for t in tasks:
                t.join()

    def _syncToProfileSafe(self, profile:str, groupModList:List[str], stateGroups:Dict, stateModlists:Dict):
        """Wrapper for _syncToProfile that catches exceptions in async mode."""
        try:
            self._syncToProfile(profile, groupModList, stateGroups, stateModlists)
        except Exception as e:
            self._log.critical(f"Failed to sync to profile {profile}: {e}")

    def _syncToProfile(self, profile:str, groupModList:List[str], stateGroups:Dict, stateModlists:Dict):
        profilesPath = Path(self._strings.moProfilesPath)
        modListPath = profilesPath / profile / "modlist.txt"
        modList = loadLines(str(modListPath))

        if modList is None:
            self._log.warning(f"Could not read modlist for profile {profile}")
            return

        newList = []
        stateMods = []
        profileStateGroups = self._groups.stateGroupsForProfile(profile)
        for g in profileStateGroups:
            if g in stateGroups and g in stateModlists:
                groupInfo = stateGroups[g]
                groupList = stateModlists[g]
                syncCats = groupInfo[CATEGORIES]
                for cat in syncCats:
                    catLabel = f"-{cat}"
                    if catLabel in groupList:
                        stateMods.extend(groupList[catLabel])

        for modName in groupModList:
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
        if saveLines(str(modListPath), newList):
            self._log.debug(f"Saved {str(modListPath)}")
        else:
            self._log.warning(f"Could not save {str(modListPath)}")

    def modlistToCategories(self, modList:List[str]) -> Dict[str, List[str]]:
        # Use reversed() to avoid mutating the input list
        reversedList = list(reversed(modList))
        cats = {}
        currentCat = None
        for mod in reversedList:
            modStr = mod
            if modStr.endswith("_separator"):
                currentCat = modStr.replace("_separator","")
                cats[currentCat] = []
            elif currentCat is not None:
                cats[currentCat].append(mod)
        return cats