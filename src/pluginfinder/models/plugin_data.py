import mobase, os
from plugin_version import PluginVersion
from ...shared.shared_json import SharedJson

class PluginData(SharedJson):

    def __init__(self, jsonObject=dict):
        super().__init__(jsonObject)
        
    def identifier(self):
        return str(self.getJsonProperty("Identifier"))

    def name(self):
        return str(self.getJsonProperty("Name"))

    def description(self):
        return str(self.getJsonProperty("Description"))

    def nexusUrl(self):
        return str(self.getJsonProperty("NexusUrl"))

    def githubUrl(self):
        return str(self.getJsonProperty("GithubUrl"))

    def docsUrl(self):
        return str(self.getJsonProperty("DocsUrl"))

    def downloadUrl(self):
        return str(self.getJsonProperty("DownloadUrl"))

    def pluginPaths(self):
        return self.getJsonStringArray("PluginPath")

    def localePaths(self):
        return self.getJsonStringArray("LocalePath")

    def dataPaths(self):
        return self.getJsonStringArray("DataPath")

    def versions():
        versions = []
        data = self.getJsonArray("Versions")
        if data:
            for version in data:
                versions.append(PluginVersion(version))
            return versions 
        else:
            return None