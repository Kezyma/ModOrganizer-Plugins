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
        self._util.saveJson(groupPath)

    def createSyncGroup(self, groupName:str):
        """Creates a new sync group."""
        groups = self.loadSyncGroups()
        if groupName not in groups:
            groups[groupName] = {}
            self.saveSyncGroups(groups)
        
    def updateSyncgroup(self, groupName:str, profileList:list):
        """Updates the profiles in a sync group."""
        groups = self.loadSyncGroups()
        if groupName in groups:
            groups[groupName] = profileList
            self.saveSyncGroups(groups)

    def groupFromProfile(self, profile:str):
        """Finds the group a given profile is in."""
        groups = self.loadSyncGroups()
        for g in groups:
            for p in groups[g]:
                if p == profile:
                    return g
                
    def renameProfile(self, oldProfile:str, newProfile:str):
        """Renames a profile in their given group."""
        groups = self.loadSyncGroups()
        for g in groups:
            for p in groups[g]:
                if p == oldProfile:
                    groups[g].pop(groups[g].index(oldProfile))
                    groups[g].append(newProfile)
                    self.saveSyncGroups(groups)

    def groupModlist(self, group:str):
        """Gets the path to the modlist for this group."""
        fileName = group + ".txt"
        dataPath = Path(self._strings.psGroupDataPath()) / fileName
        return str(dataPath)
