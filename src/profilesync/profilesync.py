import mobase, subprocess, os, json
from .modules.profilesync_paths import ProfileSyncPaths
from .modules.profilesync_files import ProfileSyncFiles
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path

try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class ProfileSync():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.paths = ProfileSyncPaths(self.organiser)
        self.files = ProfileSyncFiles(self.organiser)
        self.utilities = SharedUtilities()
        super().__init__()

    _syncGroups = None
    def getSyncGroups(self):
        if self._syncGroups:
            return self._syncGroups
        if self.paths.profileSyncGroupJsonFile().exists():
            try:
                with open(str(self.paths.profileSyncGroupJsonFile()), 'r') as r:
                    data = json.load(r)
                    self._syncGroups = data
            except:
                self._syncGroups = {}
        else:
            self._syncGroups = {}
        return self._syncGroups

    def saveSyncGroups(self, data):
        self._syncGroups = data
        with open(str(self.paths.profileSyncGroupJsonFile()), 'w') as r:
            json.dump(data, r)

    def addSyncGroup(self, groupName=str):
        groups = self.getSyncGroups()
        if groupName not in groups.keys():
            groups[groupName] = {}
            groups[groupName]["Profiles"] = []
        self.saveSyncGroups(groups)

    def removeSyncGroup(self, groupName=str):
        groups = self.getSyncGroups()
        if groupName in groups.keys():
            groups.pop(groupName)
        self.saveSyncGroups(groups)
        if self.paths.profileSyncGroupModlist(groupName).exists():
            self.utilities.deletePath(str(self.paths.profileSyncGroupModlist(groupName)))

    def addProfileToGroup(self, groupName=str, profileName=str):
        groups = self.getSyncGroups()
        if groupName in groups.keys():
            if profileName not in groups[groupName]["Profiles"]:
                groups[groupName]["Profiles"].append(profileName)
        self.saveSyncGroups(groups)
        if len(groups[groupName]["Profiles"]) == 1:
            self.syncToGroup(profileName) # First addition, construct the initial group modlist.
        elif len(groups[groupName]["Profiles"]) > 1:
            self.syncToProfiles(groupName) # Further additions need to sync immediately.

    def syncToGroup(self, profileName=str):
        self.organiser.refresh(True)
        groups = self.getSyncGroups()
        g = self.getProfileGroup(profileName)
        qInfo("Sync from Profile " + profileName + " to Group " + g)
        mods, enabled = self.profileModlist(profileName)
        self.setGroupModlist(g, mods)

    def syncToProfiles(self, groupName=str):
        groups = self.getSyncGroups()
        if groupName in groups.keys():
            profiles = groups[groupName]["Profiles"]
            for profile in profiles:
                self.groupToProfile(groupName, profile)
        self.organiser.refresh()
    
    def getProfileGroup(self, profileName=str):
        groups = self.getSyncGroups()
        for g in groups.keys():
            if profileName in groups[g]["Profiles"]:
                return g
        return ""

    def groupToProfile(self, groupName=str, profileName=str):
        qInfo("Sync from Group " + groupName + " to Profile " + profileName)
        groupList = self.getGroupModlist(groupName)
        mods, enabled = self.profileModlist(profileName)
        results = []
        for mod in groupList:
            if mod in enabled:
                results.append("+" + mod)
            else:
                results.append("-" + mod)
        results.reverse()
        path = self.paths.profileModlistPath(profileName)
        with open(str(path), "w") as w:
            w.writelines(results)

    def removeProfileFromGroup(self, groupName=str, profileName=str):
        groups = self.getSyncGroups()
        if groupName in groups.keys():
            if profileName in groups[groupName]["Profiles"]:
                groups[groupName]["Profiles"].remove(profileName)
            if len(groups[groupName]["Profiles"]) == 0:
                self.setGroupModlist(groupName, [])
        self.saveSyncGroups(groups)

    def groupedProfiles(self, excludeGroup=str):
        groups = self.getSyncGroups()
        used = []
        for group in groups.keys():
            if group != excludeGroup:
                used = used + groups[group]["Profiles"]
        return used

    def renameProfile(self, oldName=str, newName=str):
        groups = self.getSyncGroups()
        for group in groups.keys():
            if oldName in groups[group]["Profiles"]:
                groups[group]["Profiles"].append(newName)
                groups[group]["Profiles"].remove(oldName)
        self.saveSyncGroups(groups)

    def getGroupModlist(self, groupName=str):
        groupList = self.paths.profileSyncGroupModlist(groupName)
        if groupList.exists():
            with open(str(groupList), "r") as r:
                return r.readlines()
        else:
            return []

    def setGroupModlist(self, groupName, modList):
        groupList = self.paths.profileSyncGroupModlist(groupName)
        if not groupList.exists():
            groupList.touch()
        with open(str(groupList), "w") as w:
            w.writelines(modList)

    def profileModlist(self, profileName):
        path = self.paths.profileModlistPath(profileName)
        mods = []
        enabled = []
        if path.exists():
            with open(str(path), "r") as r:
                allmods = r.readlines()
                allmods.reverse()
                for x in allmods:
                    if x[:1] in ["+", "-"]:
                        if x[:1] == "+":
                            enabled.append(x[1:])
                        mods.append(x[1:])
        return mods, enabled

    