import mobase
from pathlib import Path
from functools import cached_property
from ....common.common_strings import CommonStrings

class RootBuilderStrings(CommonStrings):
    """Root Builder strings module, contains strings used by Root Builder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    @cached_property
    def rbOverwritePath(self) -> str:
        """Gets the path to the Root folder in the current overwrite folder."""
        return str(Path(self.moOverwritePath, "Root").absolute())

    @cached_property
    def rbDataPath(self) -> str:
        """Gets the path to any current build data for the selected game and version."""
        gamePath = self.pathSafeString(self.gamePath)
        gameVer = self.pathSafeString(self.gameVersion)
        safePath = Path(self.pluginDataPath, gamePath, gameVer)
        return str(safePath.absolute())

    
    @cached_property
    def rbCachePath(self) -> str:
        """Gets the path to the game cache for the current game and version."""
        return str(Path(self.rbDataPath, "GameData.json").absolute())
    
    @cached_property
    def rbBackupPath(self) -> str:
        """Gets the path to the backup folder for the current game and version."""
        return str(Path(self.rbDataPath, "Backup").absolute())
    
    @cached_property
    def rbBuildDataPath(self) -> str:
        """Gets the path to the current build data."""
        return str(Path(self.rbDataPath, "BuildData.json").absolute())

    @cached_property
    def rbUpdateFilePath(self) -> str:
        """Gets the path to the file used for checking Root Builder updates."""
        return str(Path(self.pluginDataPath, "VersionManifest.json"))
