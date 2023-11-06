from typing import TypedDict, Dict, List, Optional
from typing import *

VERSION = "Version"
RELEASED = "Released"
MINSUPPORT = "MinSupport"
MAXSUPPORT = "MaxSupport"
MINWORKING = "MinWorking"
MAXWORKING = "MaxWorking"
RELEASENOTES = "ReleaseNotes"
DOWNLOADURL = "DownloadUrl"
PLUGINPATH = "PluginPath"
LOCALEPATH = "LocalePath"
DATAPATH = "DataPath"

class VersionData(TypedDict):
    Version: str
    Released: str
    MinSupport: Optional[str]
    MaxSupport: Optional[str]
    MinWorking: Optional[str]
    MaxWorking: Optional[str]
    ReleaseNotes: Optional[List[str]]
    DownloadUrl: str
    PluginPath: List[str]
    LocalePath: Optional[List[str]]
    DataPath: Optional[List[str]]
    