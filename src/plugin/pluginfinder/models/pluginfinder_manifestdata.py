from typing import TypedDict, Dict, List
from typing_extensions import TypedDict, NotRequired
from .pluginfinder_versiondata import VersionData

NAME = "Name"
AUTHOR = "Author"
DESCRIPTION = "Description"
NEXUSURL = "NexusUrl"
GITHUBURL = "GithubUrl"
DOCSURL = "DocsUrl"
VERSIONS = "Versions"

class ManifestData(TypedDict):
    Name: str
    Author: str
    Description: str
    NexusUrl: NotRequired[str]
    GithubUrl: NotRequired[str]
    DocsUrl: NotRequired[str]
    Versions: List[VersionData]


