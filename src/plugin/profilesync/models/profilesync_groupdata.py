from typing import TypedDict, Dict, List
from .profilesync_stategroupdata import *

STATEGROUPS = "StateGroups"
PROFILES = "Profiles"

class GroupData(TypedDict):
    StateGroups: Dict[str, StateGroupData]
    Profiles: List[str]
    

