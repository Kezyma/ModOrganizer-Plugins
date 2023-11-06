import mobase, os
from pathlib import Path
from .profilesync_strings import ProfileSyncStrings
from ..core.profilesync_settings import ProfileSyncSettings
from .profilesync_groups import ProfileSyncGroups
from ....common.common_utilities import loadJson, deleteFile
from ....common.common_log import CommonLog
from ..models.profilesync_groupdata import *

class ProfileSyncLegacy:
    """Profile Sync legacy module, handles migration from old versions."""

    def __init__(self, organiser: mobase.IOrganizer, strings: ProfileSyncStrings, settings: ProfileSyncSettings, groups: ProfileSyncGroups, log: CommonLog) -> None:
        self._organiser = organiser
        self._strings = strings
        self._log = log
        self._settings = settings
        self._groups = groups

    def migrate(self):
        """Migrates an old v1 config to v2."""
        pDataPath = Path(self._strings.pluginDataPath)
        pFileName = "profile_sync_groups.json"
        gamePath = self._strings.gamePath
        safeGamePath = self._strings.pathSafeString("_".join(os.path.normpath(gamePath).split(os.path.sep)))
        instance = self._strings.moInstanceName
        if instance == "":
            instance = "Portable"
        else:
            instance = safeGamePath
        
        groupFilePath = pDataPath / instance / pFileName
        if groupFilePath.exists():
            oldData = loadJson(str(groupFilePath))
            if oldData is not None:
                newData = self._groups.loadSyncGroups()
                for k in oldData:
                    if k not in newData:
                        newData[k] = GroupData({
                            PROFILES: oldData[k][PROFILES],
                            STATEGROUPS: {}
                        })
                self._groups.saveSyncGroups(newData)
            deleteFile(str(groupFilePath))
