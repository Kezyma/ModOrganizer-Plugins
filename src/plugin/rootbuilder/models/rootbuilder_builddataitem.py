from ....base.base_object import BaseObject

class BuildDataItem(BaseObject):
        
    def __init__(self, dict:dict):
        super().__init__(dict)

    _SOURCE = "Source"
    def source(self, set=None) -> str:
        return self.prop(self._SOURCE, set)
    
    _RELATIVE = "Relative"
    def relative(self, set=None) -> str:
        return self.prop(self._RELATIVE, set)
    
    _HASH = "Hash"
    def hash(self, set=None) -> str:
        return self.prop(self._HASH, set)