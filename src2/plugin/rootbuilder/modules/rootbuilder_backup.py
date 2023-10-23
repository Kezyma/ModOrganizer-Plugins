import mobase
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
        backupPath = self._strings.rbBackupPath()
        return Path(backupPath).exists()
    
    def deleteBackup(self) -> bool:
        """Deletes the current backup if it exists."""
        backupPath = self._strings.rbBackupPath()
        return self._util.deleteFolder(backupPath)
    
    def createBackup(self):
        """Creates a new full backup of valid game files."""
        gameFiles = self._cache.cachedValidRootGameFiles()
        self.createPartialBackup(gameFiles, True)
        
    def updateBackup(self, overwrite=False):
        """Updates the current backup of valid game files."""
        gameFiles = self._cache.cachedValidRootGameFiles()
        self.createPartialBackup(gameFiles, overwrite)

    def createPartialBackup(self, paths:List[str], overwrite=False):
        """Creates a backup of a specific list of game paths."""
        gamePath = self._strings.gamePath()
        backupPath = self._strings.rbBackupPath()
        for file in paths:
            relativePath = self._paths.relativePath(gamePath, file)
            fullBackupPath = Path(backupPath) / relativePath
            fullGamePath = Path(gamePath) / relativePath
            if not fullBackupPath.exists() or overwrite:
                if fullGamePath.exists():
                    backupString = str(fullBackupPath.absolute())
                    if self._util.copyFile(str(fullGamePath), backupString):
                        self._log.debug("Backed up " + str(fullGamePath) + " to " + backupString)
                    else:
                        self._log.warning("Failed to back up " + str(fullGamePath) + " to " + backupString)

    def restoreBackup(self):
        """Restores every possible file from the backup."""
        gameFiles = self._cache.cachedValidRootGameFiles()
        gamePath = Path(self._strings.gamePath())
        backupPath = Path(self._strings.rbBackupPath())
        for file in gameFiles:
            if not Path(file).exists():
                relativePath = self._paths.relativePath(str(gamePath), file)
                backupFilePath = backupPath / relativePath
                if backupFilePath.exists():
                    if self._util.copyFile(str(backupFilePath), file):
                        self._log.debug("Restored file from " + str(backupFilePath) + " to " + file)
                    else:
                        self._log.warning("Failed to restore file from " + str(backupFilePath) + " to " + file)
                else:
                    self._log.info("Missing file has no backup " + file)
