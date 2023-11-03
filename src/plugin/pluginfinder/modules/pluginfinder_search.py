import mobase, threading, datetime
from .pluginfinder_strings import PluginFinderStrings
from .pluginfinder_directory import PluginFinderDirectory
from .pluginfinder_install import PluginFinderInstall
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog
from pathlib import Path

class PluginFinderSearch():
    """Plugin Finder search module, handles search and filter of the directory."""

    def __init__(self, organiser:mobase.IOrganizer, strings:PluginFinderStrings, directory:PluginFinderDirectory, install:PluginFinderInstall, util:CommonUtilities, log:CommonLog):
        self._strings = strings
        self._util = util
        self._log = log
        self._organiser = organiser
        self._directory = directory
        self._install = install

    def searchDirectory(self, searchTerms:str, installed=None, update=None, supported=None, working=None):
        manifests = self._directory.loadManifests()
        order = sorted(list(manifests.keys()), key=self.pluginDate, reverse=True)
        res = {}
        for id in order:
            manifest = manifests[id]
            isValid = True
            # Text Search
            if searchTerms != None and searchTerms != "":
                if (searchTerms.lower() not in manifest[self._directory.NAME].lower() and
                    searchTerms.lower() not in manifest[self._directory.DESCRIPTION].lower() and
                    searchTerms.lower() not in manifest[self._directory.AUTHOR].lower()):
                    isValid = False

            # Is Installed
            if installed != None:
                if installed:
                    isValid = isValid and self.pluginInstalled(id)

            # Needs Update
            if update != None:
                if update:
                    isValid = isValid and self.pluginNeedsUpdate(id)

            # Supported
            if supported != None:
                if supported:
                    isValid = isValid and self.pluginIsSupported(id)

            if working != None:
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
        current = mobase.VersionInfo(str(installedData[pluginId][self._install.VERSION]))
        return current < latest
    
    MINSUPPORT = "MinSupport"
    MAXSUPPORT = "MaxSupport"
    MINWORKING = "MinWorking"
    MAXWORKING = "MaxWorking"
    RELEASED = "Released"

    def pluginIsSupported(self, pluginId:str):
        supported = True
        pluginData = self._directory.getPluginManifest(pluginId)
        latestVersion = self._directory.getLatestVersion(pluginId)
        moVersion = self._organiser.appVersion()
        for ver in pluginData[self._directory.VERSIONS]:
            if latestVersion == mobase.VersionInfo(ver[self._directory.VERSION]):
                if self.MINSUPPORT in ver and ver[self.MINSUPPORT] != "":
                    minVer = mobase.VersionInfo(ver[self.MINSUPPORT])
                    supported = supported and moVersion >= minVer
                if self.MAXSUPPORT in ver and ver[self.MAXSUPPORT] != "":
                    maxVer = mobase.VersionInfo(ver[self.MAXSUPPORT])
                    supported = supported and moVersion <= maxVer
        return supported

    def pluginIsWorking(self, pluginId:str):
        supported = True
        pluginData = self._directory.getPluginManifest(pluginId)
        latestVersion = self._directory.getLatestVersion(pluginId)
        moVersion = self._organiser.appVersion()
        for ver in pluginData[self._directory.VERSIONS]:
            if latestVersion == mobase.VersionInfo(ver[self._directory.VERSION]):
                if self.MINWORKING in ver and ver[self.MINWORKING] != "":
                    minVer = mobase.VersionInfo(ver[self.MINWORKING])
                    supported = supported and moVersion >= minVer
                if self.MAXWORKING in ver and ver[self.MAXWORKING] != "":
                    maxVer = mobase.VersionInfo(ver[self.MAXWORKING])
                    supported = supported and moVersion <= maxVer
        return supported

    def pluginDate(self, pluginId:str):
        pluginData = self._directory.getPluginManifest(pluginId)
        latestVersion = self._directory.getLatestVersion(pluginId)
        for ver in pluginData[self._directory.VERSIONS]:
            if latestVersion == mobase.VersionInfo(ver[self._directory.VERSION]):
                dateParts = ver[self.RELEASED].split("-")
                return datetime.date(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))

        


