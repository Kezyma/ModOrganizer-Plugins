import mobase, threading
from .pluginfinder_strings import PluginFinderStrings
from ....common.common_utilities import copyFile, downloadFile, loadJson
from ....common.common_log import CommonLog
from pathlib import Path

class PluginFinderDirectory:
    """Plugin Finder directory module, handles update and loading of the directory file."""

    def __init__(self, organiser: mobase.IOrganizer, strings: PluginFinderStrings, log: CommonLog) -> None:
        self._strings = strings
        self._log = log
        self._organiser = organiser

    _remoteDirectoryUrl = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugin_directory.json"
    NAME = "Name"
    ID = "Identifier"
    MANIFEST = "Manifest"
    VERSIONS = "Versions"
    VERSION = "Version"
    DESCRIPTION = "Description"
    AUTHOR = "Author"
    GITHUB = "GithubUrl"
    NEXUS = "NexusUrl"
    DOCS = "DocsUrl"

    def initialDeploy(self):
        filePath = self._strings.pfDirectoryPath
        if not Path(filePath).exists():
            initialPath = Path(__file__).parent.parent / "data" / "pluginfinder_directory.json"
            if Path(initialPath).exists():
                copyFile(str(initialPath), str(filePath))
        nt = threading.Thread(target=self.updateDirectory)
        nt.start()

    def updateDirectory(self):
        filePath = self._strings.pfDirectoryPath
        if downloadFile(self._remoteDirectoryUrl, filePath):
            self._log.debug("Directory update downloaded.")
            self.loadDirectory(True)
        else:
            self._log.warning("Could not download directory update.")

    _directory = None
    def loadDirectory(self, reload=False) -> list:
        if self._directory is None or reload:
            filePath = self._strings.pfDirectoryPath
            self._directory = loadJson(filePath)
        return self._directory
    
    _manifests = None
    def loadManifests(self, reload=False) -> dict:
        if self._manifests is None or reload:
            directory = self.loadDirectory()
            tasks = []
            self._manifests = {}
            for ix in range(len(directory)):
                manifestInfo = directory[ix]
                manifestData = [manifestInfo[self.NAME], manifestInfo[self.ID], manifestInfo[self.MANIFEST]]
                nt = threading.Thread(target=self._loadManifest, args=manifestData)
                nt.start()
                tasks.append(nt)
            for t in tasks:
                t.join()
        return self._manifests

    def _loadManifest(self, name:str, id:str, url:str):
        manifestPath = Path(self._strings.pfManifestFolderPath)
        fileName = f"{id}.json"
        filePath = manifestPath / fileName
        if downloadFile(url, filePath):
            self._log.debug(f"Downloaded manifest from {url}")
            self._manifests[id] = loadJson(str(filePath))
        else:
            self._log.warning(f"Could not download manifest from {url}")

    def getPluginManifest(self, pluginId:str):
        manifests = self.loadManifests()
        if pluginId in manifests:
            return manifests[pluginId]
        return None
    
    def getLatestVersion(self, pluginId) -> mobase.VersionInfo:
        manifest = self.getPluginManifest(pluginId)
        versions = manifest[self.VERSIONS]
        latestVersion = None
        for v in versions:
            pver = mobase.VersionInfo(v[self.VERSION])
            if latestVersion is None:
                latestVersion = pver
            elif pver > latestVersion:
                latestVersion = pver
        return latestVersion

