import mobase
from pathlib import Path
from functools import cached_property
from ....common.common_strings import CommonStrings

class PluginFinderStrings(CommonStrings):
    """Plugin Finder strings module, contains strings used by Plugin Finder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    @cached_property
    def pfInstallDataPath(self):
        """gets the current path to install data."""
        basePath = Path(self.pluginDataPath)
        filePath = basePath / "InstallData.json"
        return str(filePath)

    @cached_property
    def pfDirectoryPath(self):
        """gets the current path to directory data."""
        basePath = Path(self.pluginDataPath)
        filePath = basePath / "Directory.json"
        return str(filePath)

    @cached_property
    def pfManifestFolderPath(self):
        """gets the current path to directory data."""
        basePath = Path(self.pluginDataPath)
        filePath = basePath / "Manifest"
        return str(filePath)

    @cached_property
    def pfStagingFolderPath(self):
        """gets the current path to directory data."""
        basePath = Path(self.pluginDataPath)
        filePath = basePath / "Staging"
        return str(filePath)

    @cached_property
    def pfCommandQueuePath(self):
        """Gets the current path to the command queue."""
        basePath = Path(self.pluginDataPath)
        filePath = basePath / "CommandQueue.bat"
        return str(filePath)

    @cached_property
    def pf7zPath(self):
        return str(Path(__file__).parent.parent / "util" / "7za.exe")
