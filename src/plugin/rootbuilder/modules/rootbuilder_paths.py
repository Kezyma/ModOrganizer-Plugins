import mobase, glob, re
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_paths import CommonPaths
from ....common.common_log import CommonLog
from typing import List

class RootBuilderPaths(CommonPaths):
    """Root Builder paths module, contains path related functions for Root Builder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:RootBuilderSettings, strings:RootBuilderStrings):
        super().__init__(plugin, organiser)
        self._strings = strings
        self._settings = settings

    def gameFiles(self)-> List[str]:
        """Gets a complete list of files in the game folder."""
        gameFolder = self._strings.gamePath
        gameFiles = self.files(gameFolder)
        return gameFiles
    
    def gameRootFiles(self)-> List[str]:
        """Gets a complete list of files in the game folder, minus the game data folder."""
        allFiles = self.gameFiles()
        #dataFolder = self._strings.gameDataPath
        #gameFolder = self._strings.gamePath
        #res = []
        #if dataFolder != gameFolder:
        #    for path in allFiles:
        #        if not self.pathShared(dataFolder, path):
        #            res.append(path)
        #else:
        #    res = allFiles
        return allFiles
    
    def validGameRootFiles(self) -> List[str]:
        """Gets a complete list of files in the game folder that are valid for Root Builder."""
        gamePath = self._strings.gamePath
        gameFiles = self.gameRootFiles()
        return self.removeExclusions(gamePath, gameFiles)
        
    def enabledRootModFolders(self) -> List[str]:
        """Gets a complete list of enabled Root mod folders."""
        modList = self._organiser.modList().allModsByProfilePriority()
        res = []
        for mod in modList:
            if self._organiser.modList().state(mod.encode('utf-16','surrogatepass').decode('utf-16')) & mobase.ModState.ACTIVE:
                modRoot = Path(self._strings.moModsPath) / mod / "Root"
                if modRoot.exists():
                    res.append(str(modRoot))
        return res
    
    def validRootFiles(self, rootPath:str) -> List[str]:
        """Gets a complete list of valid Root files in a given path."""
        allFiles = self.files(rootPath)
        return self.removeExclusions(rootPath, allFiles)
        
    def removeExclusions(self, rootPath:str, fileList:List[str]) -> List[str]:
        """Removes any exclusions from a list of files."""
        exclusions = self._settings.exclusions()
        
        excludeFiles = []
        
        for exc in exclusions:
            if exc != "":
                if not exc.startswith("r:"):
                    excludePath = str(Path(glob.escape(rootPath)) / exc)
                    for match in glob.glob(excludePath, recursive=True):
                        matchPath = Path(match)
                        if matchPath.is_file() and match in fileList:
                            excludeFiles.append(match)
                        elif matchPath.is_dir():
                            for file in self.files(match):
                                if file in fileList:
                                    excludeFiles.append(file)
                elif exc.startswith("r:"):
                    pattern = exc.replace("r:", "")
                    for file in fileList:
                        rel = self.relativePath(rootPath, file)
                        if re.match(pattern, rel):
                            if file in fileList:
                                excludeFiles.append(file)
        validFiles = []
        for f in fileList:
            if f not in excludeFiles:
                validFiles.append(f)

        return validFiles
    
    def filterFiles(self, rootPath:str, fileList:List[str], inclusions:List[str]) -> List[str]:
        """Filters a list of files specific matches."""
        validFiles = []
        returnFiles = []
        for inc in inclusions:
            if inc != "":
                if not inc.startswith("r:"):
                    excludePath = str(Path(glob.escape(rootPath)) / inc)
                    for match in glob.glob(excludePath, recursive=True):
                        matchPath = Path(match)
                        if matchPath.is_file():
                            validFiles.append(match)
                        elif matchPath.is_dir():
                            validFiles.extend(self.files(match))
                elif inc.startswith("r:"):
                    pattern = inc.replace("r:", "")
                    for file in fileList:
                        rel = self.relativePath(rootPath, file)
                        if re.match(pattern, rel):
                            validFiles.append(file)

        for file in fileList:
            if file in validFiles:
                returnFiles.append(file)
        return returnFiles
        
    def validCopyFiles(self, rootPath:str, fileList:List[str]) -> List[str]:
        """Filters a list of files to only those available for copy mode."""
        return self.filterFiles(rootPath, fileList, self._settings.copyfiles())
    
    def validLinkFiles(self, rootPath:str, fileList:List[str]) -> List[str]:
        """Filters a list of files to only those available for link mode."""
        return self.filterFiles(rootPath, fileList, self._settings.linkfiles())
    
    def validUsvfsFiles(self, rootPath:str, fileList:List[str]) -> List[str]:
        """Filters a list of files to only those available for usvfs mode."""
        return self.filterFiles(rootPath, fileList, self._settings.usvfsfiles())





