import mobase, os
from plugin_version import PluginVersion
from ...shared.shared_json import SharedJson
from ...shared.shared_utilities import SharedUtilities

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
        for version in allVersions:
            if version.maxWorking() == "" or !self.utilities.versionIsNewer(version.maxWorking(), moVersion):
                if version.minWorking() == "" or !self.utilities.versionIsNewer(moVersion, version.minWorking()):
                    workingVersions.append(version)

        latestVersion = workingVersions[0]
        latest = latestVersion.version()
        for version in workingVersions:
            if self.utilities.versionIsNewer(latest, version.version()):
                latestVersion = version
                latest = version.version()

        return latestVersion