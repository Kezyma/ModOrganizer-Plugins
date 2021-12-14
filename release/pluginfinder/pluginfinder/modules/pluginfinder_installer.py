import mobase, json, urllib.request, zipfile, os, shutil, re
from pathlib import Path
from datetime import datetime, timedelta
from itertools import islice
from .pluginfinder_paths import PluginFinderPaths
from .pluginfinder_files import PluginFinderFiles
from ...shared.shared_utilities import SharedUtilities
from ..models.plugin_data import PluginData
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class PluginFinderInstaller():

    def __init__(self, organiser=mobase.IOrganizer, paths=PluginFinderPaths, files=PluginFinderFiles):
        self.organiser = organiser
        self.paths = paths
        self.files = files
        self.utilities = SharedUtilities()
        super().__init__() 

    def installPlugin(self, plugin=PluginData):
        pluginId = plugin.identifier()
        currentVersion = plugin.current(self.organiser.appVersion().canonicalString())
        downloadUrl = currentVersion.downloadUrl()
        
        installedFiles = self.getInstalledFiles()
        if str(pluginId) not in installedFiles:
            installedFiles[str(pluginId)] = {}
        if "PluginFiles" not in installedFiles[str(pluginId)]:
            installedFiles[str(pluginId)]["PluginFiles"] = []
        if "LocaleFiles" not in installedFiles[str(pluginId)]:
            installedFiles[str(pluginId)]["LocaleFiles"] = []
        if "DataFiles" not in installedFiles[str(pluginId)]:
            installedFiles[str(pluginId)]["DataFiles"] = []
        installedFiles[str(pluginId)]["Version"] = currentVersion.version()

        qInfo("Downloading from " + downloadUrl)
        urlparts = str(downloadUrl).split(".")
        urlparts.reverse()
        extension = urlparts[0]
        destPath = str(self.paths.pluginStageTempPath()) + "." + extension
        urllib.request.urlretrieve(downloadUrl, destPath)
        
        qInfo("Extracting " + str(destPath))
        command = "\"" + str(self.paths.zipExePath()) + "\" x \"" + str(destPath) + "\" -o\"" + str(self.paths.pluginStageTempPath()) + "\" -y"
        qInfo("Executing command " + command)
        os.system(command)

        for path in currentVersion.pluginPaths():
            sourcePath = str(self.paths.pluginStageTempPath() / str(path))
            sourceName = str(os.path.basename(str(sourcePath)))
            destPath = str(self.paths.modOrganizerPluginPath() / sourceName)
            files = []
            if os.path.isfile(sourcePath):
                files.append(sourcePath)
            if os.path.isdir(sourcePath):
                files = self.files.getFolderFileList(sourcePath)
            for source in files:
                try:
                    rel = Path(sourceName) / self.paths.relativePath(sourcePath, source)
                    dest = self.paths.modOrganizerPluginPath() / rel
                    qInfo("Copying from " + str(source) + " to " + str(dest))
                    self.utilities.moveTo(source, dest)
                    if str(rel) not in installedFiles[str(pluginId)]["PluginFiles"]:
                        installedFiles[str(pluginId)]["PluginFiles"].append(str(rel))
                except:
                    qInfo("Could not install " + sourceName)
                        
        for path in currentVersion.localePaths():
            sourcePath = str(self.paths.pluginStageTempPath() / str(path))
            sourceName = str(os.path.basename(str(sourcePath)))
            destPath = str(self.paths.modOrganizerLocalePath() / sourceName)
            files = []
            if os.path.isfile(sourcePath):
                files.append(sourcePath)
            if os.path.isdir(sourcePath):
                files = self.files.getFolderFileList(sourcePath)
            for source in files:
                try:
                    rel = Path(sourceName) / self.paths.relativePath(sourcePath, source)
                    dest = self.paths.modOrganizerLocalePath() / rel
                    qInfo("Copying from " + str(source) + " to " + str(dest))
                    self.utilities.moveTo(source, dest)
                    if str(rel) not in installedFiles[str(pluginId)]["LocaleFiles"]:
                        installedFiles[str(pluginId)]["LocaleFiles"].append(str(rel))
                except:
                    qInfo("Could not install " + sourceName)
                        
        for path in currentVersion.dataPaths():
            if path not in installedFiles[str(pluginId)]["DataFiles"]:
                installedFiles[str(pluginId)]["DataFiles"].append(str(path))

        self.saveInstalledFiles(installedFiles)
        #self.utilities.deletePath(self.paths.pluginZipTempPath())
        #shutil.rmtree(self.paths.pluginStageTempPath())
        
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

    def installedVersion(self, pluginId=str):
        if self.isInstalled(pluginId):
            return self.getInstalledFiles()[str(pluginId)]["Version"]
        return ""

    def installedPlugins(self):
        return self.getInstalledFiles().keys()

    def uninstallPlugin(self, pluginId=str):
        """ Removes a plugin. """
        files = self.getInstalledFiles()

        for path in files[str(pluginId)]["PluginFiles"]:
            deletePath = self.paths.modOrganizerPluginPath() / path
            if deletePath.exists():
                qInfo("Deleting " + str(deletePath))
                if os.path.isfile(str(deletePath)):
                    self.utilities.deletePath(str(deletePath))
                if os.path.isdir(str(deletePath)):
                    shutil.rmtree(str(deletePath))

        for path in files[str(pluginId)]["LocaleFiles"]:
            deletePath = self.paths.modOrganizerLocalePath() / path
            if deletePath.exists():
                qInfo("Deleting " + str(deletePath))
                if os.path.isfile(str(deletePath)):
                    self.utilities.deletePath(str(deletePath))
                if os.path.isdir(str(deletePath)):
                    shutil.rmtree(str(deletePath))

        for path in files[str(pluginId)]["DataFiles"]:
            deletePath = self.paths.modOrganizerPluginPath() / path
            if deletePath.exists():
                qInfo("Deleting " + str(deletePath))
                if os.path.isfile(str(deletePath)):
                    self.utilities.deletePath(str(deletePath))
                if os.path.isdir(str(deletePath)):
                    shutil.rmtree(str(deletePath))

        files.pop(str(pluginId))
        self.saveInstalledFiles(files)
        
    #_versionRegex = r"VersionInfo\(\s*([0-9]*)\s*,?\s*([0-9]*)\s*,?\s*([0-9]*)\s*,?\s*([0-9]*)\s*,?\s*([A-Za-z.]*)\s*\)"
    #def getPluginVersion(self, filePath=str):
    #    fileText = str(open(str(filePath), 'r').readlines())
    #    qInfo("Scanning file text: " + fileText)
    #    findVersion = re.search(self._versionRegex, fileText, re.MULTILINE)
    #    if findVersion:
    #        qInfo("Regex match, version found.")
    #        versionString = ""

    #        major = findVersion.group(1)
    #        if major and str(major) != "":
    #            versionString += str(major)

    #        minor = findVersion.group(2)
    #        if minor and str(minor) != "":
    #            versionString += "." + str(minor)

    #        subminor = findVersion.group(3)
    #        if subminor and str(subminor) != "":
    #            versionString += "." + str(subminor)

    #        subsubminor = findVersion.group(4)
    #        if subsubminor and str(subsubminor) != "":
    #            versionString += "." + str(subsubminor)

    #        releasetype = findVersion.group(5)
    #        if releasetype and str(releasetype) != "":
    #            rel = str(releasetype).split("ReleaseType.")[1].lower()
    #            if rel != "":
    #                versionString += rel[0]
            
    #        return versionString
    #    qInfo("Regex didn't match, could not find version.")
    #    return ""

    

    

    #def hasLink(self, pluginId=str, linkName=str):
    #    return next(p for p in self.directory() if str(p["Id"]) == str(pluginId))[linkName] != ""