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
            overwritePath = Path(self.moOverwritePath(), "Root")
            self._rbOverwritePath = str(overwritePath.absolute())
        return self._rbOverwritePath
    
    _rbDataPath = str()
    def rbDataPath(self) -> str:
        """Gets the path to any current build data for the selected game and version."""
        if self._rbDataPath == str():
            gamePath = self.pathSafeString(self.gamePath())
            gameVer = self.pathSafeString(self.gameVersion())
            basePath = self.pluginDataPath()
            safePath = Path(basePath, gamePath, gameVer)
            self._rbDataPath = str(safePath.absolute())
        return self._rbDataPath
    
    _rbCachePath = str()
    def rbCachePath(self) -> str:
        """Gets the path to the game cache for the current game and version."""
        if self._rbCachePath == str():
            cachePath = Path(self.rbDataPath(), "GameData.json")
            self._rbCachePath = str(cachePath.absolute())
        return self._rbCachePath
    
    _rbBackupPath = str()
    def rbBackupPath(self) -> str:
        """Gets the path to the backup folder for the current game and version."""
        if self._rbBackupPath == str():
            backupPath = Path(self.rbDataPath(), "Backup")
            self._rbBackupPath = str(backupPath.absolute())
        return self._rbBackupPath
    
    _rbBuildDataPath = str()
    def rbBuildDataPath(self) -> str:
        """Gets the path to the current build data."""
        if self._rbBuildDataPath == str():
            buildDataPath = Path(self.rbDataPath(), "BuildData.json")
            self._rbBuildDataPath = str(buildDataPath.absolute())
        return self._rbBuildDataPath
    
