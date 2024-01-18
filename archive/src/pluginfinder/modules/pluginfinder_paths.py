import mobase, os
from ...shared.shared_paths import SharedPaths
from pathlib import Path

class PluginFinderPaths(SharedPaths):
    """ Plugin Finder path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("PluginFinder", organiser) 
        
    _modOrganizerLocalePath = str()
    def modOrganizerLocalePath(self):
        if self._modOrganizerLocalePath == str():
            self._modOrganizerLocalePath = str(self.modOrganizerPath() / "translations")
        return Path(self._modOrganizerLocalePath)

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

    
    _pluginDirectoryUrl = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugin_directory.json"
    def pluginDirectoryUrl(self):
        """ Url to the directory json for updating. """
        return self._pluginDirectoryUrl

    _initialDirectoryPath = str()
    def initialDirectoryPath(self):
        """ Path to the initial directory json to be deployed during install. """
        if self._initialDirectoryPath == str():
            self._initialDirectoryPath = str(Path(__file__).parent.parent / "plugin_directory.json")
        return self._initialDirectoryPath

    _directoryJsonPath = str()
    def directoryJsonPath(self):
        """ Path to the current plugin directory json file. """
        if self._directoryJsonPath == str():
            self._directoryJsonPath = str(self.pluginDataPath() / "plugin_directory.json")
        return Path(self._directoryJsonPath)

    _counterJsonPath = str()
    def counterJsonPath(self):
        """ Path to the current plugin counter json file. """
        if self._counterJsonPath == str():
            self._counterJsonPath = str(self.pluginDataPath() / "plugin_counters.json")
        return Path(self._counterJsonPath)

    _pluginDataCacheFolderPath = str()
    def pluginDataCacheFolderPath(self):
        """ Gets the location of the current plugin json file. """
        if self._pluginDataCacheFolderPath == str():
            self._pluginDataCacheFolderPath = self.pluginDataPath() / "directory"
        if not Path(self._pluginDataCacheFolderPath).exists():
            os.makedirs(self._pluginDataCacheFolderPath)
        return Path(self._pluginDataCacheFolderPath)
    
    def pluginDataCachePath(self, pluginId=str):
        """ Gets the location of the current plugin json file. """
        return self.pluginDataCacheFolderPath() / (str(pluginId) + ".json")

    _githubReleaseJsonCacheFolderPath = str()
    def githubReleaseJsonCacheFolderPath(self):
        """ Gets the location of the current plugin json file. """
        if self._githubReleaseJsonCacheFolderPath == str():
            self._githubReleaseJsonCacheFolderPath = self.pluginDataPath() / "github"
        if not Path(self._githubReleaseJsonCacheFolderPath).exists():
            os.makedirs(self._githubReleaseJsonCacheFolderPath)
        return Path(self._githubReleaseJsonCacheFolderPath)

    def githubReleaseJsonCachePath(self, author=str, repo=str, tag=str):
        """ Gets the location of the current plugin json file. """
        return self.githubReleaseJsonCacheFolderPath() / (str(author) + "_" + repo + "_" + tag + ".json")

    def zipExePath(self):
        """ Gets the path to 7za.exe """
        return Path(__file__).parent / "7za.exe"
