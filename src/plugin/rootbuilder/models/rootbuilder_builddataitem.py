from typing import TypedDict

SOURCE = "Source"
RELATIVE = "Relative"
HASH = "Hash"

class BuilDataItem(TypedDict):
    Source: str
    Relative: str
    Hash: str