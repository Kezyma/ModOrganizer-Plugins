import mobase, os
from plugin_version import PluginVersion

class PluginData(self):

    def __init__(self, jsonObject=dict):
        self.json = jsonObject
        super().__init__()

    def getJsonProperty(self, key=str):
        if key in self.json.keys():
            return self.json[key]
        else:
            return None

    def getJsonArray(self, key=str):
        data = self.getJsonProperty(key)
        res = []
        if data:
            try:
                for val in data:
                    res.append(data)
                return res
            except:
                return None
        else:
            return None

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

    def downloadUrl(self):
        return str(self.getJsonProperty("DownloadUrl"))

    def pluginPaths(self):
        paths = []
        data = self.getJsonArray("PluginPath")
        if data:
            for path in data:
                paths.append(str(path))
            return paths
        else:
            return None

    def localePaths(self):
        paths = []
        data = self.getJsonArray("LocalePath")
        if data:
            for path in data:
                paths.append(str(path))
            return paths
        else:
            return None

    def dataPaths(self):
        paths = []
        data = self.getJsonArray("DataPath")
        if data:
            for path in data:
                paths.append(str(path))
            return paths
        else:
            return None

    def versions():
        versions = []
        data = self.getJsonArray("Versions")
        if data:
            for version in data:
                versions.append(PluginVersion(version))
            return versions 
        else:
            return None