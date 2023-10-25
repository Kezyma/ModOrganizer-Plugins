import mobase, os
from pathlib import Path
from ...shared.shared_paths import SharedPaths

class ProfileSyncPaths(SharedPaths):
    """ Profile Sync path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("ProfileSync", organiser) 

    _profileSyncGroupJsonFile = str()
    def profileSyncGroupJsonFile(self):
        if self._profileSyncGroupJsonFile == str():
            if self.currentInstanceName() == "":
                self._profileSyncGroupJsonFile = self.pluginDataPath() / "Portable" / "profile_sync_groups.json"
            else:
                self._profileSyncGroupJsonFile = self.pluginDataPath() / self.safeGamePathName() / "profile_sync_groups.json"
        if not Path(self._profileSyncGroupJsonFile).parent.exists():
            os.makedirs(str(Path(self._profileSyncGroupJsonFile).parent))
        if not Path(self._profileSyncGroupJsonFile).exists():
            Path(self._profileSyncGroupJsonFile).touch()
        return Path(self._profileSyncGroupJsonFile)

    _profileSyncModlistFolder = str()
    def profileSyncGroupModlist(self, groupName=str):
        if self._profileSyncModlistFolder == str():
            if self.currentInstanceName() == "":
                self._profileSyncModlistFolder = self.pluginDataPath() / "Portable" / "groups"
            else:    
                self._profileSyncModlistFolder = self.pluginDataPath() / self.safeGamePathName() / "groups"
        if not Path(self._profileSyncModlistFolder).exists():
            os.makedirs(str(self._profileSyncModlistFolder))
        return Path(self._profileSyncModlistFolder) / (self.fileSafeName(str(groupName)) + ".txt")

    def profileModlistPath(self, profile=str):
        return self.modOrganizerProfilesPath() / profile / "modlist.txt"
