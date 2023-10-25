import mobase, os
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class SharedJson():

    def __init__(self, jsonObject=dict):
        self.json = jsonObject
        super().__init__()

    def getJsonProperty(self, key=str):
        try:
            return self.json[str(key)]
        except:
            return ""

    def getJsonArray(self, key=str):
        data = self.getJsonProperty(key)
        res = []
        if data:
            try:
                for val in data:
                    res.append(val)
                return res
            except:
                return []
        else:
            return None

    def getJsonStringArray(self, key=str):
        paths = []
        data = self.getJsonArray(key)
        if data:
            for path in data:
                paths.append(str(path))
            return paths
        else:
            return []