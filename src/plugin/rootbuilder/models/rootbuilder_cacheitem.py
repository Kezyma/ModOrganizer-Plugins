from typing import TypedDict, Dict

RELATIVE = "Relative"
HASH = "Hash"
MODIFIED = "Modified"
SIZE = "Size"

class CacheItem(TypedDict):
    Relative: str
    Hash: str
    Modified: float
    Size: int



