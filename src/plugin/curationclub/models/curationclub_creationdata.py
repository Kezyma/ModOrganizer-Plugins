"""Creation Club creation data model."""

from typing import TypedDict, List, Optional

# Keys for creation data
CREATION_ID = "id"
CREATION_NAME = "name"
CREATION_FILES = "files"
CREATION_DESCRIPTION = "description"
CREATION_MANUAL = "manual"  # Flag for manually added creations


class CreationData(TypedDict):
    """
    Represents a Creation Club creation.

    Attributes:
        id: The creation ID (e.g., "ccBGSSSE001")
        name: The display name (e.g., "Survival Mode")
        files: List of file patterns associated with this creation
        description: Optional description of the creation
        manual: Whether this was manually added by the user
    """
    id: str
    name: str
    files: List[str]
    description: Optional[str]
    manual: Optional[bool]


def createCreationData(id: str, name: str, files: List[str],
                       description: str = "", manual: bool = False) -> CreationData:
    """Creates a new CreationData instance."""
    return CreationData({
        CREATION_ID: id,
        CREATION_NAME: name,
        CREATION_FILES: files,
        CREATION_DESCRIPTION: description,
        CREATION_MANUAL: manual
    })
