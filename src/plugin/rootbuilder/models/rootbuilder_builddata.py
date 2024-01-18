from typing import TypedDict, Dict
from .rootbuilder_builddataitem import BuilDataItem

COPY = "Copy"
LINK = "Link"
USVFS = "USVFS"

class BuilData(TypedDict):
    Copy: Dict[str, BuilDataItem]
    Link: Dict[str, BuilDataItem]
    USVFS: Dict[str, BuilDataItem]