import mobase, threading
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import loadJson, saveJson, deleteFile, hashFile
from ....common.common_log import CommonLog

class RootBuilderData:
    """Root Builder data module containing functions revolving around the saved data file."""

    def __init__(self, organiser: mobase.IOrganizer, strings: RootBuilderStrings, paths: RootBuilderPaths, settings: RootBuilderSettings, log: CommonLog) -> None:
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._log = log

    _copyKey = "COPY"
    _linkKey = "LINK"
    _usvfsKey = "USVFS"
    _sourceKey = "Source"
    _relativeKey = "Relative"
    _hashKey = "Hash"

    def dataFileExists(self) -> bool:
        """Returns true if there is a current build data file."""
        filePath = self._strings.rbBuildDataPath
        return Path(filePath).exists()

    _data = None
    def loadDataFile(self) -> dict:
        """Loads and returns the current data file, or an empty object if none exists."""
        if self._data is not None:
            return self._data
        filePath = self._strings.rbBuildDataPath
        self._data = loadJson(filePath)
        if self._data is not None:
            return self._data
        return {
            self._copyKey: {},
            self._linkKey: {},
            self._usvfsKey: {},
        }
    
    def saveDataFile(self, data:dict) -> bool:
        """Saves new data to the current data file."""
        self._data = data
        filePath = self._strings.rbBuildDataPath
        return saveJson(filePath, self._data)
    
    def deleteDataFile(self) -> bool:
        """Deletes the current data file."""
        self._data = None
        filePath = self._strings.rbBuildDataPath
        return deleteFile(filePath)
    
    _buildData = {}
    def generateBuildData(self) -> dict:
        """Generates complete build data for the existing setup."""
        self._log.debug("Finding root mod folders.")
        modFolders = self._paths.enabledRootModFolders()
        overwriteFolder = self._strings.rbOverwritePath
        copyPriority = self._settings.copypriority()
        linkPriority = self._settings.linkpriority()
        usvfsPriority = self._settings.usvfspriority()
        modFolders.append(overwriteFolder)
        useHash = self._settings.hash()
        self._buildData = {
            self._copyKey: {},
            self._linkKey: {},
            self._usvfsKey: {},
        }
        self._log.debug("Checking root mod folders for files.")
        for mod in modFolders:
            self._log.debug(f"Checking mod: {mod}")
            rootFiles = self._paths.validRootFiles(mod)
            copyFiles = self._paths.validCopyFiles(mod, rootFiles)
            linkFiles = self._paths.validLinkFiles(mod, rootFiles)
            usvfsFiles = self._paths.validUsvfsFiles(mod, rootFiles)
            for file in copyFiles:
                if copyPriority <= linkPriority or not file in linkFiles:
                    if copyPriority <= usvfsPriority or not file in usvfsFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        self._buildData[self._copyKey][relativePath.lower()] = {
                            self._sourceKey: file,
                            self._relativeKey: relativePath,
                            self._hashKey: ""
                        }
            for file in linkFiles:
                if linkPriority < copyPriority or not file in copyFiles:
                    if linkPriority <= usvfsPriority or not file in usvfsFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        self._buildData[self._linkKey][relativePath.lower()] = {
                            self._sourceKey: file,
                            self._relativeKey: relativePath
                        }
            for file in usvfsFiles:
                if usvfsPriority < copyPriority or not file in copyFiles:
                    if usvfsPriority < linkPriority or not file in linkFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        self._buildData[self._usvfsKey][relativePath.lower()] = {
                            self._sourceKey: file,
                            self._relativeKey: relativePath 
                        }
        if useHash:
            self._log.debug("Hash enabled, hashing root mod files.")
            threads = []
            for copyFile in self._buildData[self._copyKey]:
                nt = threading.Thread(target=self._hashModFile, args=[copyFile])
                nt.start()
                threads.append(nt)
            for t in threads:
                t.join()
        return self._buildData
            
    def _hashModFile(self, fileKey:str):
        cData = self._buildData[self._copyKey][fileKey]
        srcPath = cData[self._sourceKey]
        hash = hashFile(srcPath)
        self._buildData[self._copyKey][fileKey][self._hashKey] = hash

    def mergeBuildData(self, base:dict, overwrite:dict) -> dict:
        """Overwrites older build data with new build data."""
        copyPriority = self._settings.copypriority()
        linkPriority = self._settings.linkpriority()
        usvfsPriority = self._settings.usvfspriority()

        for fileKey in overwrite[self._copyKey]:
           if copyPriority <= linkPriority or not fileKey in base[self._linkKey]:
                if copyPriority <= usvfsPriority or not fileKey in base[self._usvfsKey]:
                    base[self._copyKey][fileKey] = overwrite[self._copyKey][fileKey]
                    if fileKey in base[self._linkKey]:
                        base[self._linkKey].pop(fileKey)
                    if fileKey in base[self._usvfsKey]:
                        base[self._usvfsKey].pop(fileKey)

        for fileKey in overwrite[self._linkKey]:
           if linkPriority < copyPriority or not fileKey in base[self._copyKey]:
                if linkPriority <= usvfsPriority or not fileKey in base[self._usvfsKey]:
                    base[self._linkKey][fileKey] = overwrite[self._linkKey][fileKey]
                    if fileKey in base[self._copyKey]:
                        base[self._copyKey].pop(fileKey)
                    if fileKey in base[self._usvfsKey]:
                        base[self._usvfsKey].pop(fileKey)

        for fileKey in overwrite[self._usvfsKey]:
           if usvfsPriority < copyPriority or not fileKey in base[self._copyKey]:
                if usvfsPriority < linkPriority or not fileKey in base[self._linkKey]:
                    base[self._usvfsKey][fileKey] = overwrite[self._usvfsKey][fileKey]
                    if fileKey in base[self._copyKey]:
                        base[self._copyKey].pop(fileKey)
                    if fileKey in base[self._linkKey]:
                        base[self._linkKey].pop(fileKey)

        return base


    