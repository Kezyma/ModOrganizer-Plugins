import mobase
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog

class RootBuilderData():
    """Root Builder data module containing functions revolving around the saved data file."""

    def __init__(self, organiser:mobase.IOrganizer,strings:RootBuilderStrings,paths:RootBuilderPaths,settings:RootBuilderSettings,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._paths = paths
        self._settings = settings
        self._util = utilities
        self._log = log

    _copyKey = "COPY"
    _linkKey = "LINK"
    _usvfsKey = "USVFS"
    _sourceKey = "Source"
    _relativeKey = "Relative"

    def dataFileExists(self) -> bool:
        """Returns true if there is a current build data file."""
        filePath = self._strings.rbBuildDataPath()
        return Path(filePath).exists()

    def loadDataFile(self) -> dict:
        """Loads and returns the current data file, or an empty object if none exists."""
        filePath = self._strings.rbBuildDataPath()
        data = self._util.loadJson(filePath)
        if data != None:
            return data
        return {
            self._copyKey: {},
            self._linkKey: {},
            self._usvfsKey: {},
        }
    
    def saveDataFile(self, data:dict) -> bool:
        """Saves new data to the current data file."""
        filePath = self._strings.rbBuildDataPath()
        return self._util.saveJson(filePath, data)
    
    def deleteDataFile(self) -> bool:
        """Deletes the current data file."""
        filePath = self._strings.rbBuildDataPath()
        return self._util.deleteFile(filePath)
    
    def generateBuildData(self) -> dict:
        """Generates complete build data for the existing setup."""
        modFolders = self._paths.enabledRootModFolders()
        overwriteFolder = self._strings.rbOverwritePath()
        modFolders.append(overwriteFolder)
        buildData = {
            self._copyKey: {},
            self._linkKey: {},
            self._usvfsKey: {},
        }
        for mod in modFolders:
            rootFiles = self._paths.validRootFiles(mod)
            copyFiles = self._paths.validCopyFiles(mod, rootFiles)
            linkFiles = self._paths.validLinkFiles(mod, rootFiles)
            usvfsFiles = self._paths.validUsvfsFiles(mod, rootFiles)
            copyPriority = self._settings.copypriority()
            linkPriority = self._settings.linkpriority()
            usvfsPriority = self._settings.usvfspriority()

            for file in copyFiles:
                if copyPriority <= linkPriority or not file in linkFiles:
                    if copyPriority <= usvfsPriority or not file in usvfsFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        buildData[self._copyKey][relativePath.lower()] = {
                            self._sourceKey: file,
                            self._relativeKey: relativePath 
                        }
            for file in linkFiles:
                if linkPriority < copyPriority or not file in copyFiles:
                    if linkPriority <= usvfsPriority or not file in usvfsFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        buildData[self._linkKey][relativePath.lower()] = {
                            self._sourceKey: file,
                            self._relativeKey: relativePath 
                        }
            for file in usvfsFiles:
                if usvfsPriority < copyPriority or not file in copyFiles:
                    if usvfsPriority < linkPriority or not file in linkFiles:
                        relativePath = self._paths.relativePath(mod, file)
                        buildData[self._usvfsKey][relativePath.lower()] = {
                            self._sourceKey: file,
                            self._relativeKey: relativePath 
                        }
        return buildData
            

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


    