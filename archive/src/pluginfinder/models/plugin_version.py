import mobase, os
from ...shared.shared_json import SharedJson

class PluginVersion(SharedJson):

    def __init__(self, jsonObject=dict):
        super().__init__(jsonObject)
        
    def released(self):
        return str(self.getJsonProperty("Released"))

    def minSupport(self):
        return str(self.getJsonProperty("MinSupport"))

    def maxSupport(self):
        return str(self.getJsonProperty("MaxSupport"))

    def minWorking(self):
        return str(self.getJsonProperty("MinWorking"))

    def maxWorking(self):
        return str(self.getJsonProperty("MaxWorking"))
    
    def version(self):
        return str(self.getJsonProperty("Version"))

    def downloadUrl(self):
        return str(self.getJsonProperty("DownloadUrl"))

    def pluginPaths(self):
        return self.getJsonStringArray("PluginPath")

    def localePaths(self):
        return self.getJsonStringArray("LocalePath")

    def dataPaths(self):
        return self.getJsonStringArray("DataPath")

    def releaseNotes(self):
        return self.getJsonStringArray("ReleaseNotes")
