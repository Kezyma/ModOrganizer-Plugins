import mobase, os
from pathlib import Path
from .profilesync_strings import ProfileSyncStrings
from ..core.profilesync_settings import ProfileSyncSettings
from .profilesync_groups import ProfileSyncGroups
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog

class ProfileSyncLegacy():
    """Profile Sync legacy module, handles migration from old versions."""

    def __init__(self, organiser:mobase.IOrganizer,strings:ProfileSyncStrings,settings:ProfileSyncSettings,groups:ProfileSyncGroups,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._util = utilities
        self._log = log
        self._settings = settings
        self._groups = groups

    def migrate(self):
        """Migrates an old v1 config to v2."""
        pDataPath = Path(self._strings.pluginDataPath())
        pFileName = "profile_sync_groups.json"
        gamePath = self._strings.gamePath()
        safeGamePath = self._strings.pathSafeString("_".join(os.path.normpath(gamePath).split(os.path.sep)))
        instance = self._strings.moInsatanceName()
        if instance == "":
            instance = "Portable"
        else:
            instance = safeGamePath
        
        groupFilePath = pDataPath / instance / pFileName
        if groupFilePath.exists():
            oldData = self._util.loadJson(str(groupFilePath))
            newData = self._groups.loadSyncGroups()
            for k in oldData:
                if k not in newData:
                    newData[k] = {
                        self._groups.PROFILES: oldData[k][self._groups.PROFILES],
                        self._groups.STATEGROUPS: {}
                    }
            self._groups.saveSyncGroups(newData)
            self._util.deleteFile(str(groupFilePath))
        

            

