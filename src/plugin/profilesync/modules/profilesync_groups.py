import mobase
from pathlib import Path
from typing import List, Dict
from .profilesync_strings import ProfileSyncStrings
from ....common.common_utilities import loadJson, saveJson
from ....common.common_log import CommonLog
from ..models.profilesync_groupdata import *

class ProfileSyncGroups:
    """Profile Sync Groups module, handles recording and updating sync groups."""

    def __init__(self, organiser: mobase.IOrganizer, strings: ProfileSyncStrings, log: CommonLog) -> None:
        self._organiser = organiser
        self._strings = strings
        self._log = log

    _groups = None
    def loadSyncGroups(self) -> Dict[str, GroupData]:
        """Loads and returns the current sync groups."""
        if self._groups is not None:
            return self._groups
        groupPath = self._strings.psGroupDataPath
        if Path(groupPath).exists():
            self._groups = loadJson(groupPath)
        else:
            self._groups = {}
        return self._groups
    
    def saveSyncGroups(self, groups:Dict[str, GroupData]):
        """Saves the specified groups."""
        self._groups = groups
        groupPath = self._strings.psGroupDataPath
        saveJson(groupPath, groups)

    def createSyncGroup(self, groupName:str):
        """Creates a new sync group."""
        groups = self.loadSyncGroups()
        if groupName not in groups:
            groups[groupName] = GroupData({
                PROFILES: [],
                STATEGROUPS: {}
            })
            self.saveSyncGroups(groups)
        
    def updateSyncgroup(self, groupName:str, profileList:List[str]):
        """Updates the profiles in a sync group."""
        groups = self.loadSyncGroups()
        if groupName in groups:
            groups[groupName][PROFILES] = profileList
            self.saveSyncGroups(groups)

    def groupFromProfile(self, profile:str) -> str:
        """Finds the group a given profile is in."""
        groups = self.loadSyncGroups()
        for g in groups:
            for p in groups[g][PROFILES]:
                if p == profile:
                    return g
        return None
                
    def renameProfile(self, oldProfile:str, newProfile:str):
        """Renames a profile in their given group."""
        groups = self.loadSyncGroups()
        for g in groups:
            groupData = groups[g]
            for p in groupData[PROFILES]:
                if p == oldProfile:
                    groups[g][PROFILES].pop(groups[g][PROFILES].index(oldProfile))
                    groups[g][PROFILES].append(newProfile)
            for sg in groupData[STATEGROUPS]:
                for sp in groupData[STATEGROUPS][sg][PROFILES]:
                    if sp == oldProfile:
                        groups[g][STATEGROUPS][sg][PROFILES].pop(groups[g][STATEGROUPS][sg][PROFILES].index(oldProfile))
                        groups[g][STATEGROUPS][sg][PROFILES].append(newProfile)
        self.saveSyncGroups(groups)
                
    def groupModlist(self, group:str) -> str:
        """Gets the path to the modlist for this group."""
        fileName = f"{group}.txt"
        dataPath = Path(self._strings.psDataPath) / group / fileName
        return str(dataPath)

    def createStateGroup(self, syncGroup:str, newName:str):
        groups = self.loadSyncGroups()
        groups[syncGroup][STATEGROUPS][newName] = StateGroupData({
            PROFILES: [],
            CATEGORIES: []
        })
        self.saveSyncGroups(groups)
    
    def updateStateGroups(self, syncGroup:str, stateGroup:str, profileList:List[str], catList:List[str]):
        groups = self.loadSyncGroups()
        groups[syncGroup][STATEGROUPS][stateGroup][CATEGORIES] = catList
        groups[syncGroup][STATEGROUPS][stateGroup][PROFILES] = profileList
        self.saveSyncGroups(groups)

    def stateGroupsForProfile(self, profileName:str) -> List[str]:
        group = self.groupFromProfile(profileName)
        groups = self.loadSyncGroups()
        res = []
        if group is not None:
            groupItm = groups[group]
            for sg in groupItm[STATEGROUPS]:
                stateItm = groupItm[STATEGROUPS][sg]
                if profileName in stateItm[PROFILES]:
                    res.append(sg)
        return res
    
    def stateGroupModlist(self, syncGroup:str, stateGroup:str) -> str:
        fileName = f"{syncGroup}_{stateGroup}.txt"
        dataPath = Path(self._strings.psDataPath) / syncGroup / fileName
        return str(dataPath)