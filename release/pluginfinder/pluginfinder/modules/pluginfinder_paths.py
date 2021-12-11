import mobase, os
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
    
    _modOrganizerPluginPath = str()
    def modOrganizerPluginPath(self):
        if self._modOrganizerPluginPath == str():
            self._modOrganizerPluginPath = str(self.modOrganizerPath() / "plugins")
        return Path(self._modOrganizerPluginPath)

    _installedPluginDataPath = str()
    def installedPluginDataPath(self):
        if self._installedPluginDataPath == str():
            self._installedPluginDataPath = self.pluginDataPath() / "InstalledPlugins.json"
        return Path(self._installedPluginDataPath)

    _pluginZipTempPath = str()
    def pluginZipTempPath(self):
        if self._pluginZipTempPath == str():
            self._pluginZipTempPath = self.pluginDataPath() / "DownloadedPlugin.zip"
        return Path(self._pluginZipTempPath)

    _pluginStageTempPath = str()
    def pluginStageTempPath(self):
        if self._pluginStageTempPath == str():
            self._pluginStageTempPath = self.pluginDataPath() / "DownloadedPlugin"
        if not Path(self._pluginStageTempPath).exists():
            os.makedirs(self._pluginStageTempPath)
        return Path(self._pluginStageTempPath)