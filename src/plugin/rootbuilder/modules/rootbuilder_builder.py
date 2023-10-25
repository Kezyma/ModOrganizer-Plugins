import mobase, os
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_data import RootBuilderData
from .rootbuilder_cache import RootBuilderCache
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog
from typing import List

class RootBuilderBuilder():
    """Root Builder builder module, handles the deployment of game files."""

    def __init__(self, organiser:mobase.IOrganizer,strings:RootBuilderStrings,paths:RootBuilderPaths,settings:RootBuilderSettings,data:RootBuilderData,cache:RootBuilderCache,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._util = utilities
        self._log = log
        self._data = data
        self._cache = cache

    def deployFiles(self, data:dict, links=False):
        """Deploys a list of files via copy (or links) from build data."""
        gamePath = Path(self._strings.gamePath())
        for relativePath in data:
            pathData = data[relativePath]
            fullPath = gamePath / str(pathData[self._data._relativeKey])
            srcPath = Path(pathData[self._data._sourceKey])
            if srcPath.exists():
                if fullPath.exists():
                    if self._util.deleteFile(str(fullPath)):
                        self._log.debug("Deleted " + str(fullPath))
                    else:
                        self._log.warning("Failed to delete " + str(fullPath))
                if links:
                    if self._util.linkFile(str(srcPath), str(fullPath)):
                        self._log.debug("Linked file from " + str(srcPath) + " to " + str(fullPath))
                    else:
                        self._log.warning("Failed to link file from " + str(srcPath) + " to " + str(fullPath))
                else:
                    if self._util.copyFile(str(srcPath), str(fullPath)):
                        self._log.debug("Copied file from " + str(srcPath) + " to " + str(fullPath))
                    else:
                        self._log.warning("Failed to copy file from " + str(srcPath) + " to " + str(fullPath))


    def deployLinks(self, data:dict):
        """Deploys a list of files via links from build data."""
        self.deployFiles(data, True)

    def deployCopy(self, data:dict):
        """Deploys a list of liles via copy from build data."""
        self.deployFiles(data, False)

    def syncFiles(self) -> dict:
        """Synchronises any deployed files with Mod Organizer and returns updated build data."""
        buildData = self._data.loadDataFile()
        cacheData = self._cache.loadCacheFile()
        gameFiles = self._paths.validGameRootFiles()
        overwritePath = self._strings.rbOverwritePath()
        gamePath = self._strings.gamePath()
        for file in gameFiles:
            relativePath = self._paths.relativePath(gamePath, file)
            relativeLower = relativePath.lower()

            if relativeLower in buildData[self._data._copyKey]:
                self._log.debug("Found copied file at " + file)
                copyData = buildData[self._data._copyKey][relativeLower]
                sourceTime = os.path.getmtime(copyData[self._data._sourceKey])
                sourceSize = os.path.getsize(copyData[self._data._sourceKey])
                fileTime = os.path.getmtime(file)
                fileSize = os.path.getsize(file)
                if sourceTime != fileTime or sourceSize != fileSize:
                    if self._util.copyFile(file, copyData[self._data._sourceKey]):
                        self._log.debug("Copied file from " + file + " to " + copyData[self._data._sourceKey])
                    else:
                        self._log.warning("Failed to copy file from " + file + " to " + copyData[self._data._sourceKey])

            elif relativeLower in buildData[self._data._linkKey]:
                self._log.debug("Found link at " + file)
                linkData = buildData[self._data._linkKey][relativeLower]
                if not Path(file).samefile(Path(linkData[self._data._sourceKey])):
                    if self._util.copyFile(file, linkData[self._data._sourceKey]):
                        self._log.debug("Copied file from " + file + " to " + linkData[self._data._sourceKey])
                    else:
                        self._log.warning("Failed to copy file from " + file + " to " + linkData[self._data._sourceKey])
                    
            elif relativeLower in cacheData:
                self._log.debug("Found game file at " + file)
                gameHash = cacheData[relativeLower][self._cache._hashKey]
                if gameHash != "":
                    newHash = self._util.hashFile(file)
                    if gameHash != newHash:
                        destPath = Path(overwritePath) / relativePath
                        if self._util.copyFile(file, str(destPath)):
                            self._log.debug("Copied file from " + file + " to " + str(destPath))
                            buildData[self._data._copyKey][relativeLower] = {
                                self._data._sourceKey: str(destPath),
                                self._data._relativeKey: relativePath 
                            }
                        else:
                            self._log.warning("Failed to copy file from " + file + " to " + str(destPath))
                else:
                    self._log.debug("No hash stored for " + relativePath)
            else:
                self._log.debug("Found new file at " + file)
                destPath = Path(overwritePath) / relativePath
                if self._util.copyFile(file, str(destPath)):
                    self._log.debug("Copied file from " + file + " to " + str(destPath))
                    buildData[self._data._copyKey][relativeLower] = {
                        self._data._sourceKey: str(destPath),
                        self._data._relativeKey: relativePath 
                    }
                else:
                    self._log.warning("Failed to copy file from " + file + " to " + str(destPath))
        return buildData
    
    def clearFiles(self):
        """Clears any deployed files or links."""
        buildData = self._data.loadDataFile()
        gamePath = Path(self._strings.gamePath())
        copiedFiles = buildData[self._data._copyKey]
        linkedFiles = buildData[self._data._linkKey]
        for relativeFile in copiedFiles:
            fullPath = gamePath / str(relativeFile)
            if fullPath.exists():
                if self._util.deleteFile(str(fullPath)):
                    self._log.debug("Deleted file " + str(fullPath))
                else:
                    self._log.warning("Could not delete file " + str(fullPath))
        for relativeFile in linkedFiles:
            fullPath = gamePath / str(relativeFile)
            if fullPath.exists():
                if self._util.unlinkFile(str(fullPath)):
                    self._log.debug("Unlinked file " + str(fullPath))
                else:
                    self._log.warning("Could not unlink file " + str(fullPath))
