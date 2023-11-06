from typing import TypedDict, Dict, List, Optional
from typing import *

VERSION = "Version"
PLUGINPATH = "PluginPath"
LOCALEPATH = "LocalePath"
DATAPATH = "DataPath"

class InstallData(TypedDict):
    Version: str
    PluginPath: List[str]
    LocalePath: Optional[List[str]]
    DataPath: Optional[List[str]]