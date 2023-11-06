from typing import TypedDict, Dict, List, Optional
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
    NexusUrl: Optional[str]
    GithubUrl: Optional[str]
    DocsUrl: Optional[str]
    Versions: List[VersionData]


