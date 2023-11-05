import mobase, os, threading
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_data import RootBuilderData
from .rootbuilder_cache import RootBuilderCache
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import copyFile, linkFile, unlinkFile, hashFile, deleteFile, deleteEmptyFolders
from ....common.common_log import CommonLog

class RootBuilderBuilder:
    """Root Builder builder module, handles the deployment of game files."""

    def __init__(self, organiser: mobase.IOrganizer, strings: RootBuilderStrings, paths: RootBuilderPaths, settings: RootBuilderSettings, data: RootBuilderData, cache: RootBuilderCache, log: CommonLog) -> None:
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._log = log
        self._data = data
        self._cache = cache

    _gamePath = Path()
    def deployFiles(self, data:dict, links=False):
        """Deploys a list of files via copy (or links) from build data."""
        self._gamePath = Path(self._strings.gamePath)
        threads = []
        for relativePath in data:
            pathData = data[relativePath]
            fullPath = self._gamePath / str(pathData[self._data._relativeKey])
            srcPath = Path(pathData[self._data._sourceKey])
            if srcPath.exists():
                if links:
                    nt = threading.Thread(target=self._deployLink, args=[str(srcPath), str(fullPath)])
                    nt.start()
                    threads.append(nt)
                else:
                    nt = threading.Thread(target=self._deployCopy, args=[str(srcPath), str(fullPath)])
                    nt.start()
                    threads.append(nt)
        for t in threads:
            t.join()

    def _deployLink(self, srcPath:str, destPath:str):
        dPath = Path(destPath)
        if dPath.exists():
            if deleteFile(destPath):
                self._log.debug(f"Deleted {destPath}")
            else:
                self._log.warning(f"Failed to delete {destPath}")
        if linkFile(srcPath, destPath):
            self._log.debug(f"Linked file from {srcPath} to {destPath}")
        else:
            self._log.warning(f"Failed to link file from {srcPath} to {destPath}")

    def _deployCopy(self, srcPath:str, destPath:str):
        dPath = Path(destPath)
        if dPath.exists():
            if deleteFile(destPath):
                self._log.debug(f"Deleted {destPath}")
            else:
                self._log.warning(f"Failed to delete {destPath}")
        if copyFile(srcPath, destPath):
            self._log.debug(f"Copied file from {srcPath} to {destPath}")
        else:
            self._log.warning(f"Failed to copy file from {srcPath} to {destPath}")

    def deployLinks(self, data:dict):
        """Deploys a list of files via links from build data."""
        self.deployFiles(data, True)

    def deployCopy(self, data:dict):
        """Deploys a list of liles via copy from build data."""
        self.deployFiles(data, False)

    _buildData = {}
    _cacheData = {}
    _overwritePath = ""
    _backupPath = ""
    def syncFiles(self) -> dict:
        """Synchronises any deployed files with Mod Organizer and returns updated build data."""
        self._log.debug("Loading build and cache data.")
        self._buildData = self._data.loadDataFile()
        self._cacheData = self._cache.loadCacheFile()
        self._log.debug("Loaded build and cache data.")
        gameFiles = self._paths.validGameRootFiles()
        self._overwritePath = self._strings.rbOverwritePath
        self._gamePath = self._strings.gamePath
        hashCompare = self._settings.hash()
        self._backupPath = Path(self._strings.rbBackupPath)
        tasks = []
        self._log.debug("Checking game folder for changes.")
        for file in gameFiles:
            nt = threading.Thread(target=self._syncFile, args=[file, hashCompare])
            nt.start()
            tasks.append(nt)
        for t in tasks:
            t.join()
        return self._buildData
    
    def _syncFile(self, filePath:str, hashCompare:bool):
        relativePath = self._paths.relativePath(self._gamePath, filePath)
        relativeLower = relativePath.lower()
        if relativeLower in self._buildData[self._data._copyKey]:
            self._log.debug(f"Found copied file at {filePath}")
            copyData = self._buildData[self._data._copyKey][relativeLower]
            sourcePath = copyData[self._data._sourceKey]
            copyHash = copyData[self._data._hashKey]
            hasChanged = False
            if hashCompare and copyHash != "":
                hasChanged = copyHash != hashFile(filePath)
            else:
                sourceTime = os.path.getmtime(sourcePath)
                sourceSize = os.path.getsize(sourcePath)
                fileTime = os.path.getmtime(filePath)
                fileSize = os.path.getsize(filePath)
                hasChanged = sourceTime != fileTime or sourceSize != fileSize
            if hasChanged:
                if copyFile(filePath, sourcePath):
                    self._log.debug(f"Copied file from {filePath} to {sourcePath}")
                else:
                    self._log.warning(f"Failed to copy file from {filePath} to {sourcePath}")

        elif relativeLower in self._buildData[self._data._linkKey]:
            self._log.debug(f"Found link at {filePath}")
            linkData = self._buildData[self._data._linkKey][relativeLower]
            sourcePath = linkData[self._data._sourceKey]
            if not Path(filePath).samefile(Path(sourcePath)):
                if copyFile(filePath, sourcePath):
                    self._log.debug(f"Copied file from {filePath} to {sourcePath}")
                else:
                    self._log.warning(f"Failed to copy file from {filePath} to {sourcePath}")
                
        elif relativeLower in self._cacheData:
            self._log.debug(f"Found game file at {filePath}")
            hasChanged = False
            newHash = ""
            cacheItem = self._cacheData[relativeLower]
            cacheHash = cacheItem[self._cache._hashKey]
            if hashCompare and cacheHash != "":
                gameHash = cacheHash
                newHash = hashFile(filePath)
                hasChanged = gameHash != newHash
            else:
                bakPath = self._backupPath / relativePath
                if bakPath.exists():
                    backupTime = os.path.getmtime(str(bakPath))
                    backupSize = os.path.getsize(str(bakPath))
                    fileTime = os.path.getmtime(filePath)
                    fileSize = os.path.getsize(filePath)
                    hasChanged = backupSize != fileSize or backupTime != fileTime
            if hasChanged:
                destPath = Path(self._overwritePath) / relativePath
                if copyFile(filePath, str(destPath)):
                    self._log.debug(f"Copied file from {filePath} to {destPath}")
                    self._buildData[self._data._copyKey][relativeLower] = {
                        self._data._sourceKey: str(destPath),
                        self._data._relativeKey: relativePath,
                        self._data._hashKey: newHash
                    }
                else:
                    self._log.warning(f"Failed to copy file from {filePath} to {destPath}")
        else:
            self._log.debug(f"Found new file at {filePath}")
            destPath = Path(self._overwritePath) / relativePath
            newHash = ""
            if hashCompare:
                newHash = hashFile(str(filePath))
            if copyFile(filePath, str(destPath)):
                self._log.debug(f"Copied file from {filePath} to {destPath}")
                self._buildData[self._data._copyKey][relativeLower] = {
                    self._data._sourceKey: str(destPath),
                    self._data._relativeKey: relativePath,
                    self._data._hashKey: newHash
                }
            else:
                self._log.warning(f"Failed to copy file from {filePath} to {destPath}")

    def clearFiles(self):
        """Clears any deployed files or links."""
        buildData = self._data.loadDataFile()
        self._gamePath = Path(self._strings.gamePath)
        copiedFiles = buildData[self._data._copyKey]
        linkedFiles = buildData[self._data._linkKey]
        threads = []
        for relativeFile in copiedFiles:
            nt = threading.Thread(target=self._clearCopy, args=[relativeFile])
            nt.start()
            threads.append(nt)
        for relativeFile in linkedFiles:
            nt = threading.Thread(target=self._clearLink, args=[relativeFile])
            nt.start()
            threads.append(nt)
        for t in threads:
            t.join()
        self.folderCleanup()

    def _clearLink(self, linkPath:str):
        fullPath = self._gamePath / str(linkPath)
        if fullPath.exists():
            if unlinkFile(str(fullPath)):
                self._log.debug(f"Unlinked file {fullPath}")
            else:
                self._log.warning(f"Could not unlink file {fullPath}")
    
    def _clearCopy(self, copyPath:str):
        fullPath = self._gamePath / str(copyPath)
        if fullPath.exists():
            if deleteFile(str(fullPath)):
                self._log.debug(f"Deleted file {fullPath}")
            else:
                self._log.warning(f"Could not delete file {fullPath}")

    def folderCleanup(self):
        gamePath = self._strings.gamePath
        deleteEmptyFolders(gamePath)

    