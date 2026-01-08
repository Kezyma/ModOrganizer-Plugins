import mobase, threading
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from ..models.rootbuilder_builddata import *
from ..models.rootbuilder_builddataitem import *
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import *
from ....common.common_log import CommonLog

class RootBuilderData:
    """Root Builder data module containing functions revolving around the saved data file."""

    def __init__(self, organiser: mobase.IOrganizer, strings: RootBuilderStrings, paths: RootBuilderPaths, settings: RootBuilderSettings, log: CommonLog) -> None:
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._log = log
        self._data = None
        self._buildData = {}
        self._buildDataLock = threading.Lock()

    def dataFileExists(self) -> bool:
        """Returns true if there is a current build data file."""
        filePath = self._strings.rbBuildDataPath
        return Path(filePath).exists()

    def loadDataFile(self) -> BuilData:
        """Loads and returns the current data file, or an empty object if none exists."""
        if self._data is not None:
            return self._data
        filePath = self._strings.rbBuildDataPath
        self._data = BuilData(loadJson(filePath))
        if self._data is not None:
            return self._data
        return BuilData({ COPY:{}, LINK:{}, USVFS:{}})
    
    def saveDataFile(self, data:BuilData) -> bool:
        """Saves new data to the current data file."""
        self._data = data
        filePath = self._strings.rbBuildDataPath
        return saveJson(filePath, self._data)
    
    def deleteDataFile(self) -> bool:
        """Deletes the current data file."""
        self._data = None
        filePath = self._strings.rbBuildDataPath
        return deleteFile(filePath)

    def generateBuildData(self) -> BuilData:
        """Generates complete build data for the existing setup."""
        self._log.debug("Finding root mod folders.")
        modFolders = self._paths.enabledRootModFolders()
        overwriteFolder = self._strings.rbOverwritePath
        copyPriority = self._settings.copypriority()
        linkPriority = self._settings.linkpriority()
        usvfsPriority = self._settings.usvfspriority()
        modFolders.append(overwriteFolder)
        useHash = self._settings.hash()
        self._buildData = BuilData({ COPY:{}, LINK:{}, USVFS:{}})
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
                        self._buildData[COPY][relativePath.lower()] = BuilDataItem({
                            SOURCE: file,
                            RELATIVE: relativePath,
                            HASH: ""
                        })
            for file in linkFiles:
                if linkPriority < copyPriority or not file in copyFiles:
                    if linkPriority <= usvfsPriority or not file in usvfsFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        self._buildData[LINK][relativePath.lower()] = BuilDataItem({
                            SOURCE: file,
                            RELATIVE: relativePath
                        })
            for file in usvfsFiles:
                if usvfsPriority < copyPriority or not file in copyFiles:
                    if usvfsPriority < linkPriority or not file in linkFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        self._buildData[USVFS][relativePath.lower()] = BuilDataItem({
                            SOURCE: file,
                            RELATIVE: relativePath 
                        })
        if useHash:
            self._log.debug("Hash enabled, hashing root mod files.")
            threads = []
            for copyFile in self._buildData[COPY]:
                nt = threading.Thread(target=self._hashModFile, args=[copyFile])
                nt.start()
                threads.append(nt)
            for t in threads:
                t.join()
        return self._buildData
            
    def _hashModFile(self, fileKey:str):
        with self._buildDataLock:
            cData = self._buildData[COPY][fileKey]
            srcPath = cData[SOURCE]
        fileHash = hashFile(srcPath)
        with self._buildDataLock:
            self._buildData[COPY][fileKey][HASH] = fileHash

    def mergeBuildData(self, base:BuilData, overwrite:BuilData) -> BuilData:
        """Overwrites older build data with new build data."""
        copyPriority = self._settings.copypriority()
        linkPriority = self._settings.linkpriority()
        usvfsPriority = self._settings.usvfspriority()

        for fileKey in overwrite[COPY]:
           if copyPriority <= linkPriority or not fileKey in base[LINK]:
                if copyPriority <= usvfsPriority or not fileKey in base[USVFS]:
                    base[COPY][fileKey] = overwrite[COPY][fileKey]
                    if fileKey in base[LINK]:
                        base[LINK].pop(fileKey)
                    if fileKey in base[USVFS]:
                        base[USVFS].pop(fileKey)

        for fileKey in overwrite[LINK]:
           if linkPriority < copyPriority or not fileKey in base[COPY]:
                if linkPriority <= usvfsPriority or not fileKey in base[USVFS]:
                    base[LINK][fileKey] = overwrite[LINK][fileKey]
                    if fileKey in base[COPY]:
                        base[COPY].pop(fileKey)
                    if fileKey in base[USVFS]:
                        base[USVFS].pop(fileKey)

        for fileKey in overwrite[USVFS]:
           if usvfsPriority < copyPriority or not fileKey in base[COPY]:
                if usvfsPriority < linkPriority or not fileKey in base[LINK]:
                    base[USVFS][fileKey] = overwrite[USVFS][fileKey]
                    if fileKey in base[COPY]:
                        base[COPY].pop(fileKey)
                    if fileKey in base[LINK]:
                        base[LINK].pop(fileKey)

        return base


    