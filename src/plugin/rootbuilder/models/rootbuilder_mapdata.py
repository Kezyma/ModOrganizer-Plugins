from typing import TypedDict, Dict, List

ROOTMAP = "RootMaps"
DATAMAP = "DataMaps"
ROOTEXT = "RootExt"
DATAEXT = "DataExt"
INVALID = "InvalidMaps"
IGNORE = "IgnoreMaps"

class MapData(TypedDict):
    RootMaps: Dict[str, str]
    DataMaps: List[str]
    RootExt: List[str]
    DataExt: List[str]
    InvalidMaps: List[str]
    IgnoreMaps: List[str]




