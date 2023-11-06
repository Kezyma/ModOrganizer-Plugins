import mobase, os, subprocess, re
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

    _needRestart = False
    _commandQueue = []
    def installBat(self, source:str, dest:str) -> str:
        return f'move /Y "{source}" "{dest}"\n'
    
    def uninstallBat(self, source:str) -> str:
        return f'del /F /Q "{source}"\n'
    
    def moKillBat(self) -> str:
        return f'C:/Windows/system32/taskkill.exe /IM ModOrganizer.exe\n'
    
    def moStartBat(self) -> str:
        return f'explorer "{self._strings.moExecutablePath}"\n'
    
    def reloadData(self):
        if self._needRestart or len(self._commandQueue) > 0:
            newQueue = [ "@echo off\n", self.moKillBat(), "timeout /t 3 /nobreak\n" ]
            newQueue.extend(self._commandQueue)
            newQueue.append(self.moStartBat())
            saveLines(self._strings.pfCommandQueuePath, newQueue)
            os.startfile(self._strings.pfCommandQueuePath)

    def installPlugin(self, pluginId:str):
        """Installs a plugin from the directory."""
        manifest = self._directory.getPluginManifest(pluginId)
        latestVer = self._directory.getLatestVersion(pluginId)
        allVer = manifest[VERSIONS]
        success = True
        for ver in allVer:
            versionItm = mobase.VersionInfo(ver[VERSION])
            # Only install the latest version.
            if versionItm == latestVer:
                url = ver[DOWNLOADURL]
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
                                    success = False
                                    self._commandQueue.append(self.installBat(str(file), str(new)))
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
                                        success = False
                                        self._commandQueue.append(self.installBat(str(file), str(new)))
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
                    if success:
                        deleteFolder(str(tempPath))
                    else:
                        self._commandQueue.append(self.uninstallBat(str(tempPath)))

                    # Remove the download
                    deleteFile(str(tempName))

                    self._needRestart = True
                else:
                    self._log.warning(f"Could not download {url}")

    def uninstallPlugin(self, pluginId:str):
        """Uninstalls a currently installed plugin."""
        installData = self.loadInstallData()
        pluginData = installData[pluginId]
        pluginPath = Path(self._strings.moPluginsPath)
        localePath = Path(self._strings.moLocalePath)
        for locale in pluginData[LOCALEPATH]:
            path = localePath / locale
            if path.exists():
                if path.is_dir() and deleteFolder(str(path)):
                    self._log.debug(f"Deleted {path}")
                elif path.is_file() and deleteFile(str(path)):
                    self._log.debug(f"Deleted {path}")
                else:
                    self._commandQueue.append(self.uninstallBat(str(path)))
                    self._log.warning(f"Could not delete {str(path)}")
        for plugin in pluginData[PLUGINPATH]:
            path = pluginPath / plugin
            if path.exists():
                if path.is_dir() and deleteFolder(str(path)):
                    self._log.debug(f"Deleted {path}")
                elif path.is_file() and deleteFile(str(path)):
                    self._log.debug(f"Deleted {path}")
                else:
                    self._commandQueue.append(self.uninstallBat(str(path)))
                    self._log.warning(f"Could not delete {str(path)}")
        for data in pluginData[DATAPATH]:
            path = pluginPath / data
            if path.exists():
                if path.is_dir() and deleteFolder(str(path)):
                    self._log.debug(f"Deleted {path}")
                elif path.is_file() and deleteFile(str(path)):
                    self._log.debug(f"Deleted {path}")
                else:
                    self._commandQueue.append(self.uninstallBat(str(path)))
                    self._log.warning(f"Could not delete {str(path)}")

        installData.pop(pluginId, None)
        self.saveInstallData(installData)
        self._needRestart = True

    def detectCurrentPlugins(self):
        self.detectInstalled()
        self.detectUninstalled()

    _verRegex = r".*VersionInfo\([\s]*([0-9]*),?[\s]*([0-9]*),?[\s]*([0-9]*),?[\s]*([0-9]*),?[\s]*(?:mobase.)?(?:ReleaseType.)?([A-Z]*)[\s]*\).*"
    _strVerRegex = r'.*VersionInfo\([\s]*"([^"]*)",?[\s]*(?:mobase.)?(?:ReleaseType.)?([A-Z]*)[\s*]*\).*'
    def detectInstalled(self):
        """Attempts to detect already installed plugins."""
        manifests = self._directory.loadManifests()
        installed = self.loadInstallData()
        foundAny = False
        for key in manifests:
            self._log.debug(f"Checking for {key}")
            manifest = manifests[key]
            isInstalled = key in installed
            if not isInstalled:
                self._log.debug(f"{key} not marked as installed.")
                searchPaths = []
                latest = self._directory.getLatestVersion(key)
                pluginPath = Path(self._strings.moPluginsPath)
                for version in manifest[VERSIONS]:
                    if mobase.VersionInfo(version[VERSION]) == latest:
                        for path in version[PLUGINPATH]:
                            baseName = os.path.basename(path)
                            fullPath = pluginPath / baseName
                            if fullPath.is_dir():
                                fullPath = fullPath / "__init__.py"
                            if fullPath.is_file():
                                if str(fullPath).endswith(".py"):
                                    searchPaths.append(str(fullPath))

                        for path in searchPaths:
                            self._log.debug(f"Checking for file {path}")
                            if Path(path).exists() and not isInstalled:
                                self._log.debug(f"File exists!")
                                pluginVersion = None
                                isModular = os.path.basename(path) == "__init__.py"
                                if isModular:
                                    self._log.debug("Modular plugin, finding all files.")
                                    parentPath = str(Path(path).parent)
                                    allFiles = self._paths.files(parentPath)
                                    for file in allFiles:
                                        if str(file).endswith(".py"):
                                            self._log.debug(f"Checking file for version {file}")
                                            if pluginVersion is None:
                                                pluginVersion = self.findVersionInFile(file)
                                else:
                                    self._log.debug(f"Checking file for version {path}")
                                    pluginVersion = self.findVersionInFile(path)
                                if pluginVersion is None:
                                    self._log.debug("No version found.")
                                    pluginVersion = mobase.VersionInfo(0,0,0,1, mobase.ReleaseType.PRE_ALPHA)
                                pluginPaths = []
                                localePaths = []
                                for path in version[PLUGINPATH]:
                                    pluginPaths.append(os.path.basename(path))
                                for path in version[LOCALEPATH]:
                                    localePaths.append(os.path.basename(path))
                                newData = InstallData({
                                    VERSION: pluginVersion.canonicalString(),
                                    DATAPATH: version[DATAPATH],
                                    LOCALEPATH: localePaths,
                                    PLUGINPATH: pluginPaths
                                })
                                installed[key] = newData
                                isInstalled = True
                                foundAny = True
        if foundAny:
            self.saveInstallData(installed)

    def detectUninstalled(self):
        """Attempts to detect plugins that have been manually removed."""
        manifests = self._directory.loadManifests()
        installed = self.loadInstallData()
        removed = []
        for key in installed.keys():
            confirmed = False
            manifest = manifests[key]
            latest = self._directory.getLatestVersion(key)
            pluginPath = Path(self._strings.moPluginsPath)
            for version in manifest[VERSIONS]:
                if mobase.VersionInfo(version[VERSION]) == latest:
                    pluginPaths = version[PLUGINPATH]
                    for path in pluginPaths:
                        fullPath = pluginPath / path
                        if fullPath.exists():
                            confirmed = True
            if not confirmed:
                removed.append(key)
        for r in removed:
            installed.pop(r, None)
        self.saveInstallData(installed)

    def findVersionInFile(self, filePath:str) -> mobase.VersionInfo:
        version = None
        #try:
        allLines = loadLines(filePath)
        for line in allLines:
            strMatch = re.match(self._strVerRegex, line)
            if strMatch:
                self._log.debug("Found string version match.")
                groups = match.groups()
                glen = len(groups)
                verStr = groups[0]
                if glen > 1:
                    verStr = f"{verStr}{groups[1]}"
                version = mobase.VersionInfo(verStr)
            match = re.match(self._verRegex, line)
            if match:
                self._log.debug("Found version match.")
                groups = match.groups()
                glen = len(groups)
                verStr = groups[0]
                if glen > 1:
                    verStr = f"{verStr}.{groups[1]}"
                if glen > 2:
                    verStr = f"{verStr}.{groups[2]}"
                if glen > 3:
                    verStr = f"{verStr}.{groups[3]}"
                if glen > 4:
                    verStr = f"{verStr}{groups[2]}"
                version = mobase.VersionInfo(verStr)
        #except:
        #    self._log.debug(f"Could not read file {filePath}")
        return version

    def installFromFile(self, filePath:str):
        """Installs a plugin from a file."""

    def treeIsPlugin(self, tree:mobase.IFileTree):
        """Determines if a tree is an MO2 plugin installer."""
        # Load manifests
        # For each manifest
            # Get the plugin path
            # If the path is a folder, look for the final folder in the path and check it contains __init__.py
            # If the path is a file, look for that specific .py file in the tree