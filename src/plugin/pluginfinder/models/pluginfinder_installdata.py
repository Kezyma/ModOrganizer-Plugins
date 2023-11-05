from typing import TypedDict, Dict, List
from typing_extensions import TypedDict, NotRequired
from typing import *

VERSION = "Version"
PLUGINPATH = "PluginPath"
LOCALEPATH = "LocalePath"
DATAPATH = "DataPath"

class InstallData(TypedDict):
    Version: str
    PluginPath: List[str]
    LocalePath: NotRequired[List[str]]
    DataPath: NotRequired[List[str]]