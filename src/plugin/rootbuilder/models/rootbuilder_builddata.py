from ....base.base_object import BaseObject

class BuildData(BaseObject):
        
    def __init__(self, dict:dict):
        super().__init__(dict)

    _COPY = "COPY"
    def copy(self, set=None) -> dict:
        return self.prop(self._COPY, set)
    
    _LINK = "LINK"
    def link(self, set=None) -> dict:
        return self.prop(self._LINK, set)
    
    _USVFS = "USVFS"
    def usvfs(self, set=None) -> dict:
        return self.prop(self._USVFS, set)
