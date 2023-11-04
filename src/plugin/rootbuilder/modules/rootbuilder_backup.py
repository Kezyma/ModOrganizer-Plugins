import mobase, threading
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_cache import RootBuilderCache
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog
from typing import List

class RootBuilderBackup():
    """Root Builder backup module, handles the backing up and restoring of game files."""

    def __init__(self, organiser:mobase.IOrganizer,strings:RootBuilderStrings,paths:RootBuilderPaths,settings:RootBuilderSettings,cache:RootBuilderCache,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._util = utilities
        self._log = log
        self._cache = cache

    def backupExists(self) -> bool:
        """Returns true if there are currently files backed up."""
        backupPath = self._strings.rbBackupPath
        return Path(backupPath).exists()
    
    def deleteBackup(self) -> bool:
        """Deletes the current backup if it exists."""
        backupPath = self._strings.rbBackupPath
        return self._util.deleteFolder(backupPath)
    
    def createBackup(self):
        """Creates a new full backup of valid game files."""
        gameFiles = self._cache.cachedValidRootGameFiles()
        self.createPartialBackup(gameFiles, True)
        
    def updateBackup(self, overwrite=False):
        """Updates the current backup of valid game files."""
        gameFiles = self._cache.cachedValidRootGameFiles()
        self.createPartialBackup(gameFiles, overwrite)

    _overwrite = False
    _gamePath = Path()
    _backupPath = Path()
    def createPartialBackup(self, paths:List[str], overwrite=False):
        """Creates a backup of a specific list of game paths."""
        self._gamePath = Path(self._strings.gamePath)
        self._backupPath = Path(self._strings.rbBackupPath)
        self._overwrite = overwrite
        threads = []
        for path in paths:
            nt = threading.Thread(target=self._backupFile, args=[path])
            nt.start()
            threads.append(nt)
        for t in threads:
            t.join()

    def _backupFile(self, filePath:str):
        """Backs up a single file to the specified backup path."""
        relativePath = self._paths.relativePath(self._gamePath, filePath)
        fullBackupPath = self._backupPath / relativePath
        fullGamePath = self._gamePath / relativePath
        if not fullBackupPath.exists() or self._overwrite:
            if fullGamePath.exists():
                backupString = str(fullBackupPath.absolute())
                gameString = str(fullGamePath)
                if self._util.copyFile(gameString, backupString):
                    self._log.debug(f"Backed up {gameString} to {backupString}")
                else:
                    self._log.warning(f"Failed to back up {gameString} to {backupString}")

    def restoreBackup(self):
        """Restores every possible file from the backup."""
        gameFiles = self._cache.cachedValidRootGameFiles()
        self._gamePath = Path(self._strings.gamePath)
        self._backupPath = Path(self._strings.rbBackupPath)
        threads = []
        for path in gameFiles:
            nt = threading.Thread(target=self._restoreFile, args=[path])
            nt.start()
            threads.append(nt)
        for t in threads:
            t.join()
            
    def _restoreFile(self, filePath:str):
        """Restores a single file."""
        if not Path(filePath).exists():
            relativePath = self._paths.relativePath(str(self._gamePath), filePath)
            backupFilePath = self._backupPath / relativePath
            if backupFilePath.exists():
                backupString = str(backupFilePath)
                if self._util.copyFile(backupString, filePath):
                    self._log.debug(f"Restored file from {backupString} to {filePath}")
                else:
                    self._log.warning(f"Failed to restore file from {backupString} to {filePath}")
            else:
                self._log.info(f"Missing file has no backup {filePath}")
