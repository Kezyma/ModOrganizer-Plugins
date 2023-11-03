import mobase
from pathlib import Path
from ....common.common_strings import CommonStrings

class PluginFinderStrings(CommonStrings):
    """Plugin Finder strings module, contains strings used by Plugin Finder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    _pfInstallDataPath = str()
    def pfInstallDataPath(self):
        """gets the current path to install data."""
        if self._pfInstallDataPath == str():
            basePath = Path(self.pluginDataPath())
            filePath = basePath / "InstallData.json"
            self._pfInstallDataPath = str(filePath)
        return self._pfInstallDataPath
    
    _pfDirectoryPath = str()
    def pfDirectoryPath(self):
        """gets the current path to directory data."""
        if self._pfDirectoryPath == str():
            basePath = Path(self.pluginDataPath())
            filePath = basePath / "Directory.json"
            self._pfDirectoryPath = str(filePath)
        return self._pfDirectoryPath
    
    _pfManifestDirectory = str()
    def pfManifestFolderPath(self):
        """gets the current path to directory data."""
        if self._pfManifestDirectory == str():
            basePath = Path(self.pluginDataPath())
            filePath = basePath / "Manifest"
            self._pfManifestDirectory = str(filePath)
        return self._pfManifestDirectory
    
    _pfStagingDirectory = str()
    def pfStagingFolderPath(self):
        """gets the current path to directory data."""
        if self._pfStagingDirectory == str():
            basePath = Path(self.pluginDataPath())
            filePath = basePath / "Staging"
            self._pfStagingDirectory = str(filePath)
        return self._pfStagingDirectory
    
    _7zPath = str()
    def pf7zPath(self):
        if self._7zPath == str():
            sZ = Path(__file__).parent.parent / "util" / "7za.exe"
            self._7zPath =  str(sZ)
        return self._7zPath



