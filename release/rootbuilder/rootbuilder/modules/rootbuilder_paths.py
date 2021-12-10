import mobase, os, glob
from pathlib import Path
from ...shared.shared_paths import SharedPaths

class RootBuilderPaths(SharedPaths):
    """ Root Builder path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("RootBuilder", organiser)   

    _rootOverwritePath = str()
    def rootOverwritePath(self):
        """ Gets the path to root folder from within the overwrite folder. """
        if self._rootOverwritePath == str():
            self._rootOverwritePath = Path(self.organiser.overwritePath()) / "Root"
        return Path(self._rootOverwritePath)

    _rootBackupPath = str()
    def rootBackupPath(self):
        """ Gets the path to the backup folder for the current game. """
        if self._rootBackupPath == str():
            self._rootBackupPath = Path(self.rootBuilderGameDataPath()) / "backup"
        if not Path(self._rootBackupPath).exists():
            os.makedirs(self._rootBackupPath)
        return Path(self._rootBackupPath)

    _rootBuilderLegacyGameDataPath = str()
    def rootBuilderLegacyGameDataPath(self):
        """ Gets the path to the RootBuilder data folder for the current game. LEGACY. """
        if self._rootBuilderLegacyGameDataPath == str():
            self._rootBuilderLegacyGameDataPath = self.pluginDataPath() / self.safeGamePathName() 
        if not Path(self._rootBuilderLegacyGameDataPath).exists():
            os.makedirs(self._rootBuilderLegacyGameDataPath)
        return Path(self._rootBuilderLegacyGameDataPath)

    _rootBuilderGameDataPath = str()
    def rootBuilderGameDataPath(self):
        """ Gets the path to the RootBuilder data folder for the current game. """
        if self._rootBuilderGameDataPath == str():
            self._rootBuilderGameDataPath = self.pluginDataPath() / self.safeGamePathName() / self.safeVersionName(self.gameVersion())
        if not Path(self._rootBuilderGameDataPath).exists():
            os.makedirs(self._rootBuilderGameDataPath)
        return Path(self._rootBuilderGameDataPath)

    _rootCacheFilePath = str()
    def rootCacheFilePath(self):
        """ Gets the path to the cache file for the current game. """
        if self._rootCacheFilePath == str():
            self._rootCacheFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderCacheData.json")
        return Path(self._rootCacheFilePath)

    _rootBackupDataFilePath = str()
    def rootBackupDataFilePath(self):
        """ Gets the path to the current backup data file. """
        if self._rootBackupDataFilePath == str():
            self._rootBackupDataFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderBackupData.json")
        return Path(self._rootBackupDataFilePath)

    _rootModDataFilePath = str()
    def rootModDataFilePath(self):
        """ Gets the path to the current mod data file. """
        if self._rootModDataFilePath == str():
            self._rootModDataFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderModData.json")
        return Path(self._rootModDataFilePath)

    _rootLinkDataFilePath = str()
    def rootLinkDataFilePath(self):
        """ Gets the path to the current link data file. """
        if self._rootLinkDataFilePath == str():
            self._rootLinkDataFilePath = self.rootBuilderGameDataPath() / Path("RootBuilderLinkData.json")
        return Path(self._rootLinkDataFilePath)

    def rootRelativePath(self, path):
        """ Gets the part of a path relative to the Root folder. """
        return Path(str(path)[(str(os.path.abspath(Path(path))).lower().find(os.path.sep + "root") + 6):])

    def rootCacheFilePathAllVersions(self):
        """ Gets all cache files for all versions of the game. """
        searchPath = self.rootBuilderLegacyGameDataPath() / "*" / Path("RootBuilderCacheData.json")
        return glob.glob(str(searchPath))
    
    def rootBackupDataFilePathAllVersions(self):
        """ Gets all backup data files for all versions of the game. """
        searchPath = self.rootBuilderLegacyGameDataPath() / "*" / Path("RootBuilderBackupData.json")
        return glob.glob(str(searchPath))
    
    def rootModDataFilePathAllVersions(self):
        """ Gets all mod data files for all versions of the game. """
        searchPath = self.rootBuilderLegacyGameDataPath() / "*" / Path("RootBuilderModData.json")
        return glob.glob(str(searchPath))
    
    def rootLinkDataFilePathAllVersions(self):
        """ Gets all link data files for all versions of the game. """
        searchPath = self.rootBuilderLegacyGameDataPath() / "*" / Path("RootBuilderLinkData.json")
        return glob.glob(str(searchPath))

    def rootBackupPathAllVersions(self):
        """ Gets all backup folders for all versions of the game. """
        searchPath = self.rootBuilderLegacyGameDataPath() / "*" / "backup"
        return glob.glob(str(searchPath))
    
        