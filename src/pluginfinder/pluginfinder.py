import mobase, json, urllib.request, zipfile, os, shutil, re
from ..shared.shared_utilities import SharedUtilities
from .modules.pluginfinder_paths import PluginFinderPaths
from .modules.pluginfinder_files import PluginFinderFiles
from PyQt5.QtCore import QCoreApplication, qInfo
from pathlib import Path

# TODO: Check for updates function to get all installed plugins again and check if the version has changed. 
# TODO: Search function to filter plugins by text
# TODO: Uninstall needs to check for pluginData[plugin]["Data"] and remove those files/folders as well, if any exist.
# TODO: Restart Mod Organizer if a plugin has been installed.
# TODO: Add install for translation files as well.
# TODO: Update data schema
#[
#    {
#        "PluginID": "someid",
#        "ManifestUrl": "url.to.github.manifest.file"
#    },
#    {
#        "PluginID": "someid",
#        "ManifestUrl": "url.to.github.manifest.file"
#    }
#]
#{
#    "Name": "plugin name",
#    "Author": "plugin author",
#    "Description": "plugin description",
#    "NexusUrl": "nexus url",
#    "GithubUrl": "github url",
#    "Download": "url.to.download.zip.for.plugin",
#    "InstallPaths": [ "path/to/plugin/files/or/folders" ],
#    "DataPaths": [ "path/to/plugin/data/files/or/folders" ],
#    "TranslationPaths": [ "path/to/translation/files/to/install"],
#    "Versions": [
#        {
#            "Version": "versionnum",
#            "SupportsMin": "minMOversion",
#            "SupportsMax": "maxMOversion",
#            "Download": "url.to.download.zip.for.plugin",
#            "InstallPaths": [ "path/to/plugin/files/or/folders" ],
#            "DataPaths": [ "path/to/plugin/data/files/or/folders" ],
#            "TranslationPaths": [ "path/to/translation/files/to/install"]
#        }
#    ]
#}

# Update PF to download a json file containing names and links to each plugin's manifest json file
# Retrieve the plugin manifest json only for plugins on the current page.
# Add paging system in place of the scrollbar.
# Add a search box at the top that filters based on the name in the central json file.
# Actually delete files in the DataFiles field on uninstall.
# Add a versions field with an array of information on version support, use this if it exists, then fallback to the default values and get the version the hacky way.
# Add localeFiles field with an array of files to be installed and uninstalled from localisations.
# Add version checking to see if plugins need updating and display current + new version.
# Restart ModOrganizer when PF is closed after a plugin was installed or uninstalled.

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
            installedFiles[str(pluginId)] = {}
        if "Files" not in installedFiles[str(pluginId)]:
            installedFiles[str(pluginId)]["Files"] = []

        versionOptions = []
        for pluginPath in pluginData["Path"]:
            filePath = str(self.paths.pluginStageTempPath() / str(pluginPath))
            if os.path.isfile(filePath):
                if filePath.endswith(".py"):
                    version = self.getPluginVersion(filePath)
                    if version != "":
                        qInfo("Found version " + str(version))
                        versionOptions.append(version)
                fileName = str(os.path.basename(str(filePath)))
                destPath = self.paths.modOrganizerPluginPath() / fileName
                qInfo("Copying file " + str(filePath) + " to" + str(destPath))
                self.utilities.copyTo(str(filePath), str(destPath))
                if fileName not in installedFiles[str(pluginId)]["Files"]:
                    installedFiles[str(pluginId)]["Files"].append(fileName)
            if os.path.isdir(filePath):
                allFiles = self.files.getFolderFileList(str(filePath))
                folderName = str(Path(os.path.basename(str(filePath))))
                for subFilePath in allFiles:
                    if str(subFilePath).endswith(".py"):
                        qInfo("Checking file for version " + str(subFilePath))
                        version = self.getPluginVersion(subFilePath)
                        if version != "":
                            qInfo("Found version " + str(version))
                            versionOptions.append(version)
                    relativePath = str(Path(folderName) / self.paths.relativePath(str(filePath), str(subFilePath)))
                    destPath = self.paths.modOrganizerPluginPath() / relativePath
                    qInfo("Copying file " + str(subFilePath) + " to " + str(destPath))
                    self.utilities.copyTo(str(subFilePath), str(destPath))
                    if relativePath not in installedFiles[str(pluginId)]["Files"]:
                        installedFiles[str(pluginId)]["Files"].append(relativePath)
                installedFiles[str(pluginId)]["Files"].append(folderName)

        distinctVersions = []
        for ver in versionOptions:
            if ver not in distinctVersions:
                distinctVersions.append(ver)

        if len(distinctVersions) > 0:
            distinctVersions.sort(reverse = True)
            installedFiles[str(pluginId)]["Version"] = str(distinctVersions[0])
        else:
            installedFiles[str(pluginId)]["Version"] = ""
            
        self.saveInstalledFiles(installedFiles)

        self.utilities.deletePath(self.paths.pluginZipTempPath())
        shutil.rmtree(self.paths.pluginStageTempPath())

    def uninstall(self, pluginId=str):
        """ Removes a plugin. """
        qInfo("Uninstalling "+ str(pluginId))

        fileData = self.getInstalledFiles()

        for filePath in fileData[str(pluginId)]["Files"]:
            deletePath = self.paths.modOrganizerPluginPath() / filePath
            if deletePath.exists():
                qInfo("Deleting file " + str(deletePath))
                if os.path.isfile(str(deletePath)):
                    self.utilities.deletePath(str(deletePath))
                if os.path.isdir(str(deletePath)):
                    shutil.rmtree(str(deletePath))
        fileData.pop(str(pluginId))

        self.saveInstalledFiles(fileData)

    _versionRegex = r"VersionInfo\(\s*([0-9]*)\s*,?\s*([0-9]*)\s*,?\s*([0-9]*)\s*,?\s*([0-9]*)\s*,?\s*([A-Za-z.]*)\s*\)"
    def getPluginVersion(self, filePath=str):
        fileText = str(open(str(filePath), 'r').readlines())
        qInfo("Scanning file text: " + fileText)
        findVersion = re.search(self._versionRegex, fileText, re.MULTILINE)
        if findVersion:
            qInfo("Regex match, version found.")
            versionString = ""

            major = findVersion.group(1)
            if major and str(major) != "":
                versionString += str(major)

            minor = findVersion.group(2)
            if minor and str(minor) != "":
                versionString += "." + str(minor)

            subminor = findVersion.group(3)
            if subminor and str(subminor) != "":
                versionString += "." + str(subminor)

            subsubminor = findVersion.group(4)
            if subsubminor and str(subsubminor) != "":
                versionString += "." + str(subsubminor)

            releasetype = findVersion.group(5)
            if releasetype and str(releasetype) != "":
                rel = str(releasetype).split("ReleaseType.")[1].lower()
                if rel != "":
                    versionString += rel[0]
            
            return versionString
        qInfo("Regex didn't match, could not find version.")
        return ""

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
