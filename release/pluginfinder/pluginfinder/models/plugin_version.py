import mobase, os

class PluginVersion(self):

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
        
    def released(self):
        return str(self.getJsonProperty("Released"))

    def minSupport(self):
        return str(self.getJsonProperty("MinSupport"))

    def maxSupport(self):
        return str(self.getJsonProperty("MaxSupport"))
    
    def version(self):
        return str(self.getJsonProperty("Version"))

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
