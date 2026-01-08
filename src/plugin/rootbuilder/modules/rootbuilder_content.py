import mobase
from ....common.common_log import CommonLog
from ....common.common_icons import ROOTBUILDER_CONTENT_ICON_PATH


class RootBuilderDataContent(mobase.ModDataContent):
    """
    ModDataContent GameFeature that shows Root Builder content indicator.

    Displays an icon in MO2's Content column for mods containing
    a 'Root' folder at the top level, indicating the mod uses
    Root Builder for game root file deployment.

    This is not a plugin - it's a GameFeature that gets registered by
    RootBuilderAutobuild during initialization.
    """

    # Content type ID (use high number to avoid conflicts with built-in types)
    CONTENT_ROOTBUILDER = 16384

    def __init__(self, log: CommonLog):
        super().__init__()
        self._log = log

    def getAllContents(self) -> list:
        """
        Returns all content types this feature can detect.

        Returns:
            List containing a single Content object for Root Builder content.
        """
        return [
            mobase.ModDataContent.Content(
                self.CONTENT_ROOTBUILDER,
                "Root Content",
                ROOTBUILDER_CONTENT_ICON_PATH
            )
        ]

    def getContentsFor(self, tree: mobase.IFileTree) -> list:
        """
        Analyzes a mod's file tree to detect Root Builder content.

        Args:
            tree: The file tree representing the mod's directory structure.

        Returns:
            List of content IDs present in the mod. Returns [CONTENT_ROOTBUILDER]
            if a Root folder is found at the top level, empty list otherwise.
        """
        for entry in tree:
            if entry.isDir() and entry.name().lower() == "root":
                self._log.debug(f"Found Root Builder content in mod")
                return [self.CONTENT_ROOTBUILDER]

        return []
