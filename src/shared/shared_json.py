import mobase, os

class SharedJson(self):

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

    def getJsonStringArray(self, key=str):
        paths = []
        data = self.getJsonArray(key)
        if data:
            for path in data:
                paths.append(str(path))
            return paths
        else:
            return None