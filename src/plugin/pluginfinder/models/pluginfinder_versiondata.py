from typing import TypedDict, Dict, List
from typing_extensions import TypedDict, NotRequired
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
    MinSupport: NotRequired[str]
    MaxSupport: NotRequired[str]
    MinWorking: NotRequired[str]
    MaxWorking: NotRequired[str]
    ReleaseNotes: NotRequired[List[str]]
    DownloadUrl: str
    PluginPath: List[str]
    LocalePath: NotRequired[List[str]]
    DataPath: NotRequired[List[str]]
    