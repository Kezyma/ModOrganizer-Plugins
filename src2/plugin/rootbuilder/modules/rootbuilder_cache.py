import mobase
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog
from typing import List

class RootBuilderCache():
    """Root Builder cache module, handles the hashing and recording of game files."""

    def __init__(self, organiser:mobase.IOrganizer,strings:RootBuilderStrings,paths:RootBuilderPaths,settings:RootBuilderSettings,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._util = utilities
        self._log = log

    def cacheFileExists(self) -> bool:
        """Returns true if there is a current build data file."""
        filePath = self._strings.rbCachePath()
        return Path(filePath).exists()

    def loadCacheFile(self):
        """Loads and returns the current cache file, or an empty object if none exists."""
        filePath = self._strings.rbCachePath()
        data = self._util.loadJson(filePath)
        if data != None:
            return data
        return {}
    
    def saveCacheFile(self, data:dict) -> bool:
        """Saves new data to the current cache file."""
        filePath = self._strings.rbCachePath()
        return self._util.saveJson(filePath, data)
    
    def deleteCacheFile(self) -> bool:
        """Deletes the current cache file."""
        filePath = self._strings.rbCachePath()
        return self._util.deleteFile(filePath)
    
    def cachedValidRootGameFiles(self) -> List[str]:
        """Gets the list of game files from cache, or from the raw files if none exists."""
        if self.cacheFileExists():
            gamePath = self._strings.gamePath()
            cacheFiles = self.loadCacheFile()
            gameFiles = []
            for cacheFile in cacheFiles:
                finalPath = Path(gamePath, cacheFile)
                gameFiles.append(finalPath.absolute())
            return gameFiles
        else:
            return self._paths.validGameRootFiles()
    
    def updateCache(self) -> dict:
        """Loads the current cache file and then updates it with any changes."""
        currentCache = self.loadCacheFile()
        cacheFiles = self._paths.validGameRootFiles()
        gamePath = self._strings.gamePath()
        for file in cacheFiles:
            relativePath = self._paths.relativePath(gamePath, file).lower()
            if (relativePath not in currentCache or currentCache[relativePath] == "") and Path(file).exists():
                currentCache[relativePath] = self._util.hashFile(file)
        return currentCache

    def updateOverwriteCache(self, paths:List[str]) -> dict:
        """Loads the current cache file and then updates it with the provided overwrites."""
        currentCache = self.loadCacheFile()
        gamePath = Path(self._strings.gamePath())

        # If a cache file already exists, it's the definitive answer to all of the official game files.
        gameFiles = self.cachedValidRootGameFiles()

        # If any of these new overwrites aren't already cached, add them!
        for file in gameFiles:
            relativeLower = self._paths.relativePath(str(gamePath), file).lower()
            #fullPath = Path(file)
            #if relativeLower in paths:
                #if (relativeLower not in currentCache or currentCache[relativeLower] == "") and fullPath.exists():
                #    currentCache[relativeLower] = self._util.hashFile(str(fullPath))
            #else:
            if relativeLower not in currentCache:
                currentCache[relativeLower] = ""
        return currentCache
