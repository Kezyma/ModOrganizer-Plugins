import mobase, threading
from .pluginfinder_strings import PluginFinderStrings
from ....common.common_utilities import *
from ....common.common_log import CommonLog
from pathlib import Path
from ..models.pluginfinder_directorydata import *
from ..models.pluginfinder_manifestdata import *
from ..models.pluginfinder_versiondata import *

class PluginFinderDirectory:
    """Plugin Finder directory module, handles update and loading of the directory file."""

    def __init__(self, organiser: mobase.IOrganizer, strings: PluginFinderStrings, log: CommonLog) -> None:
        self._strings = strings
        self._log = log
        self._organiser = organiser
        self._directory = None
        self._manifests = None
        self._manifestsLock = threading.Lock()

    _remoteDirectoryUrl = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugin_directory.json"

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

    def loadDirectory(self, reload=False) -> List[DirectoryData]:
        if self._directory is None or reload:
            filePath = self._strings.pfDirectoryPath
            self._directory = loadJson(filePath)
            if self._directory is None:
                self.initialDeploy()
                # Try loading once more after initial deploy, but don't recurse infinitely
                self._directory = loadJson(filePath)
                if self._directory is None:
                    self._log.warning("Could not load plugin directory")
                    return []
        return self._directory

    def loadManifests(self, reload=False) -> Dict[str, ManifestData]:
        if self._manifests is None or reload:
            directory = self.loadDirectory()
            tasks = []
            self._manifests = {}
            for ix in range(len(directory)):
                manifestInfo = directory[ix]
                manifestData = [manifestInfo[NAME], manifestInfo[IDENTIFIER], manifestInfo[MANIFEST]]
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
        else:
            self._log.warning(f"Could not download manifest from {url}")
        if filePath.exists():
            manifestData = ManifestData(loadJson(str(filePath)))
            with self._manifestsLock:
                self._manifests[id] = manifestData


    def getPluginManifest(self, pluginId:str) -> ManifestData:
        manifests = self.loadManifests()
        if pluginId in manifests:
            return manifests[pluginId]
        return None
    
    def getLatestVersion(self, pluginId) -> mobase.VersionInfo:
        manifest = self.getPluginManifest(pluginId)
        versions = manifest[VERSIONS]
        latestVersion = None
        for v in versions:
            pver = mobase.VersionInfo(v[VERSION])
            if latestVersion is None:
                latestVersion = pver
            elif pver > latestVersion:
                latestVersion = pver
        return latestVersion
    
    def getLatestVersionData(self, pluginId) -> VersionData:
        latestVer = self.getLatestVersion(pluginId)
        manifest = self.getPluginManifest(pluginId)
        versions = manifest[VERSIONS]
        for ver in versions:
            verInfo = mobase.VersionInfo(ver[VERSION])
            if verInfo == latestVer:
                return ver

