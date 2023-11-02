import mobase
from pathlib import Path
from ....common.common_strings import CommonStrings

class ProfileSyncStrings(CommonStrings):
    """Profile Sync strings module, contains strings used by Profile Sync."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    _psDataPath = str()
    def psDataPath(self) -> str:
        """Gets the path to any current build data for the selected game."""
        if self._psDataPath == str():
            instanceName = self.pathSafeString(self.moInsatanceName())
            if instanceName == "":
                instanceName = "Portable"
            basePath = self.pluginDataPath()
            safePath = Path(basePath, instanceName)
            self._psDataPath = str(safePath.absolute())
        return self._psDataPath
    
    _psGroupDataPath = str()
    def psGroupDataPath(self) -> str:
        """Gets the path to the current group data."""
        if self._psGroupDataPath == str():
            buildDataPath = Path(self.psDataPath(), "SyncGroups.json")
            self._psGroupDataPath = str(buildDataPath.absolute())
        return self._psGroupDataPath
    
    _psUpdateFilePath = str()
    def psUpdateFilePath(self) -> str:
        """Gets the path to the file used for checking Profile Sync updates."""
        if self._psUpdateFilePath == str():
            self._psUpdateFilePath = str(Path(self.pluginDataPath(), "VersionManifest.json"))
        return self._psUpdateFilePath
