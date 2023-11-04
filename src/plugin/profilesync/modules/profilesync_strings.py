import mobase
from functools import cached_property
from pathlib import Path
from ....common.common_strings import CommonStrings

class ProfileSyncStrings(CommonStrings):
    """Profile Sync strings module, contains strings used by Profile Sync."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    @cached_property
    def psDataPath(self) -> str:
        """Gets the path to any current build data for the selected game."""
        instanceName = self.pathSafeString(self.moInstanceName)
        if instanceName == "":
            instanceName = "Portable"
        safePath = Path(self.pluginDataPath, instanceName)
        return str(safePath.absolute())
    
    @cached_property
    def psGroupDataPath(self) -> str:
        """Gets the path to the current group data."""
        return str(Path(self.psDataPath, "SyncGroups.json").absolute())

    
    @cached_property
    def psUpdateFilePath(self) -> str:
        """Gets the path to the file used for checking Profile Sync updates."""
        return str(Path(self.pluginDataPath, "VersionManifest.json"))
