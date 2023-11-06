import mobase, datetime
from .pluginfinder_strings import PluginFinderStrings
from .pluginfinder_directory import PluginFinderDirectory
from .pluginfinder_install import PluginFinderInstall
from ....common.common_log import CommonLog
from ..models.pluginfinder_versiondata import *
from ..models.pluginfinder_manifestdata import *
from ..models.pluginfinder_directorydata import *
from ..models.pluginfinder_installdata import *

class PluginFinderSearch:
    """Plugin Finder search module, handles search and filter of the directory."""

    def __init__(self, organiser: mobase.IOrganizer, strings: PluginFinderStrings, directory: PluginFinderDirectory, install: PluginFinderInstall, log: CommonLog) -> None:
        self._strings = strings
        self._log = log
        self._organiser = organiser
        self._directory = directory
        self._install = install

    def searchDirectory(self, searchTerms:str, installed:bool=None, update:bool=None, supported:bool=None, working:bool=None, sort:str=None, direction:str=None) -> Dict[str, ManifestData]:
        manifests = self._directory.loadManifests()
        reverseOrder = direction.lower() == "desc"
        if sort.lower() == "updated":
            order = sorted(list(manifests.keys()), key=self.pluginDate, reverse=reverseOrder)
        elif sort.lower() == "name":
            order = sorted(list(manifests.keys()), key=self.pluginName, reverse=reverseOrder)
        elif sort.lower() == "author":
            order = sorted(list(manifests.keys()), key=self.pluginAuthor, reverse=reverseOrder)
        res = {}
        for id in order:
            manifest = manifests[id]
            isValid = True
            # Text Search
            if searchTerms is not None and searchTerms != "":
                if (searchTerms.lower() not in manifest[NAME].lower() and
                    searchTerms.lower() not in manifest[DESCRIPTION].lower() and
                    searchTerms.lower() not in manifest[AUTHOR].lower()):
                    isValid = False

            # Is Installed
            if installed is not None:
                if installed:
                    isValid = isValid and self.pluginInstalled(id)

            # Needs Update
            if update is not None:
                if update:
                    isValid = isValid and self.pluginNeedsUpdate(id)

            # Supported
            if supported is not None:
                if supported:
                    isValid = isValid and self.pluginIsSupported(id)

            if working is not None:
                if working:
                    isValid = isValid and self.pluginIsWorking(id)

            if isValid:
                res[id] = manifests[id]
        return res

    def pluginInstalled(self, pluginId:str):
        installedData = self._install.loadInstallData()
        return pluginId in installedData.keys()
    
    def pluginNeedsUpdate(self, pluginId:str):
        installed = self.pluginInstalled(pluginId)
        if not installed:
            return False
        installedData = self._install.loadInstallData()
        latest = self._directory.getLatestVersion(pluginId)
        current = mobase.VersionInfo(str(installedData[pluginId][VERSION]))
        return current < latest

    def pluginIsSupported(self, pluginId:str):
        supported = True
        pluginData = self._directory.getPluginManifest(pluginId)
        latestVersion = self._directory.getLatestVersion(pluginId)
        moVersion = self._organiser.appVersion()
        for ver in pluginData[VERSIONS]:
            if latestVersion == mobase.VersionInfo(ver[VERSION]):
                if MINSUPPORT in ver and ver[MINSUPPORT] != "":
                    minVer = mobase.VersionInfo(ver[MINSUPPORT])
                    supported = supported and moVersion >= minVer
                if MAXSUPPORT in ver and ver[MAXSUPPORT] != "":
                    maxVer = mobase.VersionInfo(ver[MAXSUPPORT])
                    supported = supported and moVersion <= maxVer
        return supported

    def pluginIsWorking(self, pluginId:str):
        supported = True
        pluginData = self._directory.getPluginManifest(pluginId)
        latestVersion = self._directory.getLatestVersion(pluginId)
        moVersion = self._organiser.appVersion()
        for ver in pluginData[VERSIONS]:
            if latestVersion == mobase.VersionInfo(ver[VERSION]):
                if MINWORKING in ver and ver[MINWORKING] != "":
                    minVer = mobase.VersionInfo(ver[MINWORKING])
                    supported = supported and moVersion >= minVer
                if MAXWORKING in ver and ver[MAXWORKING] != "":
                    maxVer = mobase.VersionInfo(ver[MAXWORKING])
                    supported = supported and moVersion <= maxVer
        return supported

    def pluginDate(self, pluginId:str):
        pluginData = self._directory.getPluginManifest(pluginId)
        latestVersion = self._directory.getLatestVersion(pluginId)
        for ver in pluginData[VERSIONS]:
            if latestVersion == mobase.VersionInfo(ver[VERSION]):
                dateParts = ver[RELEASED].split("-")
                return datetime.date(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))
            
    def pluginName(self, pluginId:str):
        pluginData = self._directory.getPluginManifest(pluginId)
        return pluginData[NAME]
    
    def pluginAuthor(self, pluginId:str):
        pluginData = self._directory.getPluginManifest(pluginId)
        return pluginData[AUTHOR]

        


