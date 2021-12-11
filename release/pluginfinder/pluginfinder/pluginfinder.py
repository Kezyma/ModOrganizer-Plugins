import mobase, json, urllib.request, zipfile, os, shutil
from ..shared.shared_utilities import SharedUtilities
from .modules.pluginfinder_paths import PluginFinderPaths
from .modules.pluginfinder_files import PluginFinderFiles
from PyQt5.QtCore import QCoreApplication, qInfo
from pathlib import Path

class PluginFinder():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.files = PluginFinderFiles(self.organiser)
        self.paths = PluginFinderPaths(self.organiser)
        self.utilities = SharedUtilities()
        super().__init__()

    def deploy(self):
        """ Deploys the directory file to plugin data and attempts to update it. """
        # Copy the default directory over to the plugin data folder.
        jsonPath = str(Path(__file__).parent / "pluginfinder_directory.json")
        if Path(jsonPath).exists():
            self.utilities.moveTo(jsonPath, self.paths.directoryJsonPath())
        # Try and update the directory from the github repo.
        self.updateDirectory()

    def updateDirectory(self):
        """ Attempt to download a directory update from Github. """
        try:
            data = json.loads(urllib.request.urlopen(self.paths.githubDirectoryUrl).read())
            with open(self.paths.directoryJsonPath(), "w") as rcJson:
                json.dump(data, rcJson)
        except:
            qInfo("Could not download update.")
        urllib.request.urlcleanup()

    def directory(self):
        """ Get the directory as json. """
        directory = json.load(open(self.paths.directoryJsonPath()))
        return directory

    def install(self, pluginId=str):
        """ Installs a plugin. """
        qInfo("Installing " + str(pluginId))
        pluginData = next(p for p in self.directory() if str(p["Id"]) == str(pluginId))
        downloadUrl = str(pluginData["Download"])

        qInfo("Downloading from " + downloadUrl)
        urllib.request.urlretrieve(downloadUrl, self.paths.pluginZipTempPath())
        qInfo("Download complete. Extracting to " + str(self.paths.pluginStageTempPath()))
        with zipfile.ZipFile(self.paths.pluginZipTempPath(), 'r') as zip_ref:
            zip_ref.extractall(self.paths.pluginStageTempPath())
            qInfo("Extraction complete.")

        installedFiles = self.getInstalledFiles()
        if str(pluginId) not in installedFiles:
            installedFiles[str(pluginId)] = []

        for pluginPath in pluginData["Path"]:
            filePath = str(self.paths.pluginStageTempPath() / str(pluginPath))
            if os.path.isfile(filePath):
                fileName = str(os.path.basename(str(filePath)))
                destPath = self.paths.modOrganizerPluginPath() / fileName
                qInfo("Copying file " + str(filePath) + " to" + str(destPath))
                self.utilities.copyTo(str(filePath), str(destPath))
                if fileName not in installedFiles[str(pluginId)]:
                    installedFiles[str(pluginId)].append(fileName)
            if os.path.isdir(filePath):
                allFiles = self.files.getFolderFileList(str(filePath))
                folderName = str(Path(os.path.basename(str(filePath))))
                for subFilePath in allFiles:
                    relativePath = str(Path(folderName) / self.paths.relativePath(str(filePath), str(subFilePath)))
                    destPath = self.paths.modOrganizerPluginPath() / relativePath
                    qInfo("Copying file " + str(subFilePath) + " to " + str(destPath))
                    self.utilities.copyTo(str(subFilePath), str(destPath))
                    if relativePath not in installedFiles[str(pluginId)]:
                        installedFiles[str(pluginId)].append(relativePath)
                installedFiles[str(pluginId)].append(folderName)
        self.saveInstalledFiles(installedFiles)

    def uninstall(self, pluginId=str):
        """ Removes a plugin. """
        qInfo("Uninstalling "+ str(pluginId))

        fileData = self.getInstalledFiles()

        for filePath in fileData[str(pluginId)]:
            deletePath = self.paths.modOrganizerPluginPath() / filePath
            if deletePath.exists():
                qInfo("Deleting file " + str(deletePath))
                if os.path.isfile(str(deletePath)):
                    self.utilities.deletePath(str(deletePath))
                if os.path.isdir(str(deletePath)):
                    shutil.rmtree(str(deletePath))
        fileData.pop(str(pluginId))

        self.saveInstalledFiles(fileData)


    def getInstalledFiles(self):
        if self.paths.installedPluginDataPath().exists():
            fileData = json.load(open(self.paths.installedPluginDataPath()))
            return fileData
        return {}

    def saveInstalledFiles(self, files):
        if not self.paths.installedPluginDataPath().exists():
            self.paths.installedPluginDataPath().touch()
        with open(self.paths.installedPluginDataPath(), "w") as rcJson:
            json.dump(files, rcJson)

    def isInstalled(self, pluginId=str):
        files = self.getInstalledFiles()
        if str(pluginId) in files:
            return True
        return False

    def hasLink(self, pluginId=str, linkName=str):
        return next(p for p in self.directory() if str(p["Id"]) == str(pluginId))[linkName] != ""
