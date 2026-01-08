"""Curation Club curation tracking data model."""

from typing import TypedDict, List, Dict, Optional

# Keys for curation data
CURATION_ID = "id"
CURATION_NAME = "name"
CURATION_MOD_NAME = "modName"
CURATION_SOURCE_FILES = "sourceFiles"  # Original paths in game folder
CURATION_DEST_FILES = "destFiles"      # Paths in mod folder
CURATION_TIMESTAMP = "timestamp"


class CurationData(TypedDict):
    """
    Tracks a curated creation for undo purposes.

    Attributes:
        id: The creation ID
        name: The creation display name
        modName: The MO2 mod name it was moved to
        sourceFiles: Original file paths in game Data folder
        destFiles: New file paths in mod folder
        timestamp: When the curation was performed
    """
    id: str
    name: str
    modName: str
    sourceFiles: List[str]
    destFiles: List[str]
    timestamp: str


class CurationState(TypedDict):
    """
    Overall curation state tracking.

    Attributes:
        curations: Dict mapping creation ID to CurationData
        version: Schema version for future migrations
    """
    curations: Dict[str, CurationData]
    version: int


def createCurationData(id: str, name: str, modName: str,
                       sourceFiles: List[str], destFiles: List[str],
                       timestamp: str) -> CurationData:
    """Creates a new CurationData instance."""
    return CurationData({
        CURATION_ID: id,
        CURATION_NAME: name,
        CURATION_MOD_NAME: modName,
        CURATION_SOURCE_FILES: sourceFiles,
        CURATION_DEST_FILES: destFiles,
        CURATION_TIMESTAMP: timestamp
    })


def createCurationState() -> CurationState:
    """Creates a new empty CurationState."""
    return CurationState({
        "curations": {},
        "version": 1
    })
