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
        return self._util.deleteFile(backupPath)
    
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
            relativePath = self._paths.relativePath(gamePath, file).lower()
            backupPath = Path(backupPath) / relativePath
            if not backupPath.exists() or overwrite:
                backupString = str(backupPath)
                if self._util.copyFile(file, backupString):
                    self._log.debug("Backed up " + file + " to " + backupString)
                else:
                    self._log.warning("Failed to back up " + file + " to " + backupString)

    def restoreBackup(self):
        """Restores every possible file from the backup."""