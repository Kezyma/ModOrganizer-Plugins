from typing import TypedDict, Dict, List

NAME = "Name"
IDENTIFIER = "Identifier"
MANIFEST = "Manifest"

class DirectoryData(TypedDict):
    Name: str
    Identifier: str
    Manifest: str
    

