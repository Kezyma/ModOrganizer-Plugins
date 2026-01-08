import mobase
from ....common.common_log import CommonLog
from ....common.common_icons import OPENMW_CONTENT_ICON_PATH


class OpenMWPlayerDataContent(mobase.ModDataContent):
    """
    ModDataContent GameFeature that shows OpenMW content indicator.

    Displays an icon in MO2's Content column for mods containing:
    - .omwaddon files (OpenMW addon plugins)
    - .omwscripts files (OpenMW Lua scripts)
    - .omwgame files (OpenMW total conversions)
    - OpenMW-specific folders (animations, l10n, scripts, shaders)

    This is not a plugin - it's a GameFeature that gets registered by
    OpenMWPlayerLauncher during initialization when managing Morrowind/OpenMW.
    """

    # Content type ID (use high number to avoid conflicts with built-in types)
    CONTENT_OPENMW = 8192

    # Valid OpenMW-specific file extensions
    VALID_EXTENSIONS = (".omwaddon", ".omwscripts", ".omwgame")

    # Valid OpenMW-specific folders
    VALID_FOLDERS = ("animations", "l10n", "mygui", "scripts", "shaders")

    def __init__(self, log: CommonLog):
        super().__init__()
        self._log = log

    def getAllContents(self) -> list:
        """
        Returns all content types this feature can detect.

        Returns:
            List containing a single Content object for OpenMW content.
        """
        return [
            mobase.ModDataContent.Content(
                self.CONTENT_OPENMW,
                "OpenMW Content",
                OPENMW_CONTENT_ICON_PATH
            )
        ]

    def getContentsFor(self, tree: mobase.IFileTree) -> list:
        """
        Analyzes a mod's file tree to detect OpenMW content.

        Args:
            tree: The file tree representing the mod's directory structure.

        Returns:
            List of content IDs present in the mod. Returns [CONTENT_OPENMW]
            if OpenMW files or folders are found, empty list otherwise.
        """
        # Check for OpenMW file extensions
        for entry in tree:
            name = entry.name().lower()
            if name.endswith(self.VALID_EXTENSIONS):
                self._log.debug(f"Found OpenMW content file: {entry.name()}")
                return [self.CONTENT_OPENMW]

        # Check for OpenMW-specific folders
        for entry in tree:
            if entry.isDir() and entry.name().lower() in self.VALID_FOLDERS:
                self._log.debug(f"Found OpenMW content folder: {entry.name()}")
                return [self.CONTENT_OPENMW]

        return []
