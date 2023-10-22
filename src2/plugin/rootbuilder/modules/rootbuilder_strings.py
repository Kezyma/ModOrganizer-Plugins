import mobase
from pathlib import Path
from ....common.common_strings import CommonStrings

class RootBuilderStrings(CommonStrings):
    """Root Builder strings module, contains strings used by Root Builder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    _rbOverwritePath = str()
    def rbOverwritePath(self) -> str:
        """Gets the path to the Root folder in the current overwrite folder."""
        if self._rbOverwritePath == str():
            self._rbOverwritePath = str(Path(self.moOverwritePath()) / "Root")
        return self._rbOverwritePath
    
    _rbDataPath = str()
    def rbDataPath(self) -> str:
        """Gets the path to any current build data for the selected game and version."""
        if self._rbDataPath == str():
            gamePath = self.gamePath()
            gameVer = self.gameVersion()
            basePath = self.pluginDataPath()
            self._rbDataPath = str(Path(basePath) / self.pathSafeString(gamePath) / self.pathSafeString(gameVer))
        return self._rbDataPath
    
    _rbCachePath = str()
    def rbCachePath(self) -> str:
        """Gets the path to the game cache for the current game and version."""
        if self._rbCachePath == str():
            self._rbCachePath = str(Path(self.rbDataPath()) / "GameData.json")
        return self._rbCachePath
    
    _rbBackupPath = str()
    def rbBackupPath(self) -> str:
        """Gets the path to the backup folder for the current game and version."""
        if self._rbBackupPath == str():
            self._rbBackupPath = str(Path(self.rbDataPath()) / "Backup")
        return self._rbBackupPath
    
    _rbBuildDataPath = str()
    def rbBuildDataPath(self) -> str:
        """Gets the path to the current build data."""
        if self._rbBuildDataPath == str():
            self._rbBuildDataPath = str(Path(self.rbDataPath()) / "BuildData.json")
        return self._rbBuildDataPath
    
