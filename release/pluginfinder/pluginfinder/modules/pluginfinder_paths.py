import mobase
from ...shared.shared_paths import SharedPaths
from pathlib import Path

class PluginFinderPaths(SharedPaths):
    """ Plugin Finder path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("PluginFinder", organiser) 

    _directoryJsonPath = str()
    def directoryJsonPath(self):
        if self._directoryJsonPath == str():
            self._directoryJsonPath = str(self.pluginDataPath() / "pluginfinder_directory.json")
        return Path(self._directoryJsonPath)

    githubDirectoryUrl = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/src/pluginfinder/pluginfinder_directory.json"
    
