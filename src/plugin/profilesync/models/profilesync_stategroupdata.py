from typing import TypedDict, Dict, List

PROFILES = "Profiles"
CATEGORIES = "Categories"

class StateGroupData(TypedDict):
    Categories: List[str]
    Profiles: List[str]
    

