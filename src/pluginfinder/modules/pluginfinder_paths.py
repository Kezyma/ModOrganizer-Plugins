import mobase, os
from ...shared.shared_paths import SharedPaths
from pathlib import Path

class PluginFinderPaths(SharedPaths):
    """ Plugin Finder path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("PluginFinder", organiser) 
        
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

    
    _pluginDirectoryUrl = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/manifest/plugin_directory.json"
    def pluginDirectoryUrl(self):
        """ Url to the directory json for updating. """
        return self._pluginDirectoryUrl

    _initialDirectoryPath = str()
    def initialDirectoryPath(self):
        """ Path to the initial directory json to be deployed during install. """
        if self._initialDirectoryPath == str():
            self._initialDirectoryPath = str(Path(__file__).parent.parent / "plugin_directory.json")
        return self._initialDirectoryPath;

    _directoryJsonPath = str()
    def directoryJsonPath(self):
        """ Path to the current plugin directory json file. """
        if self._directoryJsonPath == str():
            self._directoryJsonPath = str(self.pluginDataPath() / "plugin_directory.json")
        return Path(self._directoryJsonPath)

    _pluginDataCachePath = str()
    def pluginDataCachePath(self, pluginId=str):
        """ Gets the location of the current plugin json file. """
        if self._pluginDataCachePath == str():
            self._pluginDataCachePath = self.pluginDataPath() / "directory"
        if not Path(self._pluginDataCachePath).exists():
            os.makedirs(self._pluginDataCachePath)
        return self._pluginDataCachePath / (str(pluginId) + ".json")
