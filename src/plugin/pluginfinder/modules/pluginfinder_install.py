import mobase, os, subprocess
from .pluginfinder_strings import PluginFinderStrings
from .pluginfinder_directory import PluginFinderDirectory
from ....common.common_utilities import *
from ....common.common_log import CommonLog
from ....common.common_paths import CommonPaths
from ..models.pluginfinder_manifestdata import *
from ..models.pluginfinder_versiondata import *
from ..models.pluginfinder_installdata import *
from pathlib import Path

class PluginFinderInstall:
    """Plugin Finder install module, handles install, update and uninstall of plugins."""

    def __init__(self, organiser:mobase.IOrganizer, strings:PluginFinderStrings, directory:PluginFinderDirectory, paths:CommonPaths, log:CommonLog) -> None:
        self._strings = strings
        self._log = log
        self._directory = directory
        self._organiser = organiser
        self._paths = paths
    
    _installData:Dict[str, InstallData] = None
    def loadInstallData(self, reload=False) -> Dict[str, InstallData]:
        if self._installData is None or reload:
            filePath = self._strings.pfInstallDataPath
            if Path(filePath).exists():
                self._installData = loadJson(filePath)
            else:
                self._installData = {}
        return self._installData
    
    def saveInstallData(self, data:dict) -> bool:
        """Saves new data to the current data file."""
        self._installData = data
        filePath = self._strings.pfInstallDataPath
        return saveJson(filePath, self._installData)

    def installPlugin(self, pluginId:str):
        """Installs a plugin from the directory."""
        manifest = self._directory.getPluginManifest(pluginId)
        latestVer = self._directory.getLatestVersion(pluginId)
        allVer = manifest[VERSIONS]
        for ver in allVer:
            versionItm = mobase.VersionInfo(ver[VERSION])
            # Only install the latest version.
            if versionItm == latestVer:
                url = ver[self.URL]
                tempName = Path(self._strings.pfStagingFolderPath) / os.path.basename(url)
                # Download the plugin from its source.
                if downloadFile(url, str(tempName)):
                    self._log.debug(f"Downloaded {url}")
                    sZ = self._strings.pf7zPath
                    tempPath = Path(self._strings.pfStagingFolderPath) / pluginId
                    unzipCommand = f'"{sZ}" x "{str(tempName)}" -o"{str(tempPath)}" -y'
                    self._log.debug(f"Unzipping {tempName}")
                    
                    # Unzip the plugin download.
                    subprocess.call(unzipCommand, shell=True, stdout=open(os.devnull, 'wb'))

                    # Copy over any plugin files.
                    pluginDest = Path(self._strings.moPluginsPath)
                    pluginFiles = []
                    for pluginFile in ver[PLUGINPATH]:
                        relativePath = tempPath / pluginFile
                        if relativePath.exists():
                            toMove = []
                            if relativePath.is_dir():
                                toMove.extend(self._paths.files(str(relativePath)))
                            else:
                                toMove.append(str(relativePath))
                            pluginFiles.append(os.path.basename(str(relativePath)))
                            relativePath = Path(relativePath).parent
                            for file in toMove:
                                rel = self._paths.relativePath(str(relativePath), str(file))
                                new = pluginDest / rel
                                if copyFile(str(file), str(new)):
                                    self._log.debug(f"Moved from {file} to {new}")
                                else:
                                    self._log.warning(f"Could not move {file} to {new}")
                        else:
                            self._log.warning(f"Could not find {relativePath}")
                    
                    # Copy over any locale files.
                    localeDest = Path(self._strings.moLocalePath)
                    localeFiles = []
                    if LOCALEPATH in ver:
                        for localeFile in ver[LOCALEPATH]:
                            relativePath = tempPath / localeFile
                            if relativePath.exists():
                                toMove = []
                                if relativePath.is_dir():
                                    toMove.extend(self._paths.files(str(relativePath)))
                                else:
                                    toMove.append(str(relativePath))
                                localeFiles.append(os.path.basename(str(relativePath)))
                                relativePath = Path(relativePath).parent
                                for file in toMove:
                                    rel = self._paths.relativePath(str(relativePath), str(file))
                                    new = localeDest / rel
                                    localeFiles.append(str(rel))
                                    if copyFile(str(file), str(new)):
                                        self._log.debug(f"Moved from {file} to {new}")
                                    else:
                                        self._log.warning(f"Could not move {file} to {new}")
                            else:
                                self._log.warning(f"Could not find {relativePath}")

                    installItem = InstallData({
                        VERSION: ver[VERSION],
                        LOCALEPATH: localeFiles,
                        PLUGINPATH: pluginFiles,
                        DATAPATH: ver[DATAPATH]
                    })
                    installData = self.loadInstallData()
                    installData[pluginId] = installItem
                    self.saveInstallData(installData)

                    # Remove the temp download
                    deleteFolder(str(tempPath))

                    # Remove the download
                    deleteFile(str(tempName))
                else:
                    self._log.warning(f"Could not download {url}")

    def uninstallPlugin(self, pluginId:str):
        """Uninstalls a currently installed plugin."""
        installData = self.loadInstallData()
        pluginData = installData[pluginId]
        pluginPath = Path(self._strings.moPluginsPath)
        localePath = Path(self._strings.moLocalePath)
        success = True
        for locale in pluginData[LOCALEPATH]:
            path = localePath / locale
            if path.exists():
                if path.is_dir() and deleteFolder(str(path)):
                    self._log.debug(f"Deleted {path}")
                elif path.is_file() and deleteFile(str(path)):
                    self._log.debug(f"Deleted {path}")
                else:
                    success = False
                    self._log.warning(f"Could not delete {path}")
        for plugin in pluginData[PLUGINPATH]:
            path = pluginPath / plugin
            if path.exists():
                if path.is_dir() and deleteFolder(str(path)):
                    self._log.debug(f"Deleted {path}")
                elif path.is_file() and deleteFile(str(path)):
                    self._log.debug(f"Deleted {path}")
                else:
                    success = False
                    self._log.warning(f"Could not delete {path}")
        for data in pluginData[DATAPATH]:
            path = pluginPath / data
            if path.exists():
                if path.is_dir() and deleteFolder(str(path)):
                    self._log.debug(f"Deleted {path}")
                elif path.is_file() and deleteFile(str(path)):
                    self._log.debug(f"Deleted {path}")
                else:
                    success = False
                    self._log.warning(f"Could not delete {path}")
        if success:
            installData.pop(pluginId, None)
            self.saveInstallData(installData)

    def installFromFile(self, filePath:str):
        """Installs a plugin from a file."""

    def treeIsPlugin(self, tree:mobase.IFileTree):
        """Determines if a tree is an MO2 plugin installer."""
        # Load manifests
        # For each manifest
            # Get the plugin path
            # If the path is a folder, look for the final folder in the path and check it contains __init__.py
            # If the path is a file, look for that specific .py file in the tree