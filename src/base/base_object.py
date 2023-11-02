class BaseObject():

    def __init__(self, dict:dict):
        self._obj = dict
        super().__init__()

    def prop(self, key:str, new=None) -> object:
        try:
            if new != None:
                self._obj[key] = new
            return self._obj[key]
        except:
            return None
        
    def get(self) -> dict:
        return self._obj