import mobase
from pathlib import Path
from .profilesync_strings import ProfileSyncStrings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog

class ProfileSyncGroups():
    """Profile Sync Groups module, handles recording and updating sync groups."""

    def __init__(self, organiser:mobase.IOrganizer,strings:ProfileSyncStrings,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._util = utilities
        self._log = log

    STATEGROUPS = "StateGroups"
    PROFILES = "Profiles"
    CATEGORIES = "Categories"

    _groups = None
    def loadSyncGroups(self) -> dict:
        """Loads and returns the current sync groups."""
        if self._groups != None:
            return self._groups
        groupPath = self._strings.psGroupDataPath()
        if Path(groupPath).exists():
            self._groups = self._util.loadJson(groupPath)
        else:
            self._groups = {}
        return self._groups
    
    def saveSyncGroups(self, groups:dict):
        """Saves the specified groups."""
        self._groups = groups
        groupPath = self._strings.psGroupDataPath()
        self._util.saveJson(groupPath, groups)

    def createSyncGroup(self, groupName:str):
        """Creates a new sync group."""
        groups = self.loadSyncGroups()
        if groupName not in groups:
            groups[groupName] = {
                self.PROFILES: [],
                self.STATEGROUPS: {}
            }
            self.saveSyncGroups(groups)
        
    def updateSyncgroup(self, groupName:str, profileList:list):
        """Updates the profiles in a sync group."""
        groups = self.loadSyncGroups()
        if groupName in groups:
            groups[groupName][self.PROFILES] = profileList
            self.saveSyncGroups(groups)

    def groupFromProfile(self, profile:str):
        """Finds the group a given profile is in."""
        groups = self.loadSyncGroups()
        for g in groups:
            for p in groups[g][self.PROFILES]:
                if p == profile:
                    return g
        return None
                
    def renameProfile(self, oldProfile:str, newProfile:str):
        """Renames a profile in their given group."""
        groups = self.loadSyncGroups()
        for g in groups:
            groupData = groups[g]
            for p in groupData[self.PROFILES]:
                if p == oldProfile:
                    groups[g][self.PROFILES].pop(groups[g][self.PROFILES].index(oldProfile))
                    groups[g][self.PROFILES].append(newProfile)
            for sg in groupData[self.STATEGROUPS]:
                for sp in groupData[self.STATEGROUPS][sg][self.PROFILES]:
                    if sp == oldProfile:
                        groups[g][self.STATEGROUPS][sg][self.PROFILES].pop(groups[g][self.STATEGROUPS][sg][self.PROFILES].index(oldProfile))
                        groups[g][self.STATEGROUPS][sg][self.PROFILES].append(newProfile)
        self.saveSyncGroups(groups)
                
    def groupModlist(self, group:str):
        """Gets the path to the modlist for this group."""
        fileName = group + ".txt"
        dataPath = Path(self._strings.psDataPath()) / group / fileName
        return str(dataPath)

    def createStateGroup(self, syncGroup:str, newName:str):
        groups = self.loadSyncGroups()
        groups[syncGroup][self.STATEGROUPS][newName] = {
            self.PROFILES: [],
            self.CATEGORIES: []
        }
        self.saveSyncGroups(groups)
    
    def updateStateGroups(self, syncGroup:str, stateGroup:str, profileList:list, catList:list):
        groups = self.loadSyncGroups()
        groups[syncGroup][self.STATEGROUPS][stateGroup][self.CATEGORIES] = catList
        groups[syncGroup][self.STATEGROUPS][stateGroup][self.PROFILES] = profileList
        self.saveSyncGroups(groups)

    def stateGroupsForProfile(self, profileName:str):
        group = self.groupFromProfile(profileName)
        groups = self.loadSyncGroups()
        res = []
        if group != "":
            groupItm = groups[group]
            for sg in groupItm[self.STATEGROUPS]:
                stateItm = groupItm[self.STATEGROUPS][sg]
                if profileName in stateItm[self.PROFILES]:
                    res.append(sg)
        return res
    
    def stateGroupModlist(self, syncGroup:str, stateGroup:str):
        fileName = syncGroup + "_" + stateGroup + ".txt"
        dataPath = Path(self._strings.psDataPath()) / syncGroup / fileName
        return str(dataPath)