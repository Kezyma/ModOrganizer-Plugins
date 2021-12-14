import mobase, os
from datetime import datetime, timedelta
from .plugin_version import PluginVersion
from ...shared.shared_json import SharedJson
from ...shared.shared_utilities import SharedUtilities
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class PluginData(SharedJson):

    def __init__(self, jsonObject=dict):
        self.utilities = SharedUtilities()
        super().__init__(jsonObject)
        
    def identifier(self):
        return str(self.getJsonProperty("Identifier"))

    def name(self):
        return str(self.getJsonProperty("Name"))

    def author(self):
        return str(self.getJsonProperty("Author"))

    def description(self):
        return str(self.getJsonProperty("Description"))

    def nexusUrl(self):
        return str(self.getJsonProperty("NexusUrl"))

    def githubUrl(self):
        return str(self.getJsonProperty("GithubUrl"))

    def docsUrl(self):
        return str(self.getJsonProperty("DocsUrl"))
    
    def versions(self):
        versions = []
        data = self.getJsonArray("Versions")
        if data:
            for version in data:
                versions.append(PluginVersion(version))
            return versions 
        else:
            return None

    def current(self, moVersion=str):
        """ The most recent working version for a given Mod Organizer version. """
        allVersions = self.versions()
        workingVersions = []
        if allVersions and len(allVersions) > 0:
            for version in allVersions:
                if version.maxWorking() == "" or not self.utilities.versionIsNewer(version.maxWorking(), moVersion):
                    if version.minWorking() == "" or not self.utilities.versionIsNewer(moVersion, version.minWorking()):
                        workingVersions.append(version)

        if len(workingVersions) > 0:
            latestVersion = workingVersions[0]
            latest = latestVersion.version()
            for version in workingVersions:
                if self.utilities.versionIsNewer(latest, version.version()):
                    latestVersion = version
                    latest = version.version()

            return latestVersion
        return None

    def latest(self):
        """ The most recent overall version. """
        allVersions = self.versions()
        if allVersions and len(allVersions) > 0:
            latestVersion = allVersions[0]
            latest = latestVersion.version()
            for version in allVersions:
                if self.utilities.versionIsNewer(latest, version.version()):
                    latestVersion = version
                    latest = version.version()
            return latestVersion
            
        return None

    def updated(self):
        current = self.current()
        if current:
            try:
                return datetime.fromisoformat(current.released())
            except:
                return None
        else:
            latest = self.latest()
            if latest:
                try:
                    return datetime.fromisoformat(latest.released())
                except:
                    return None
        return None