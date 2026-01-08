import mobase
from ....common.common_log import CommonLog


class OpenMWPlayerDataChecker(mobase.ModDataChecker):
    """
    ModDataChecker GameFeature that validates OpenMW-specific files as valid content.

    Recognizes .omwaddon, .omwscripts, and .omwgame files as valid mod content,
    preventing MO2 from showing "mod structure looks incorrect" warnings.

    This is not a plugin - it's a GameFeature that gets registered by
    OpenMWPlayerLauncher during initialization when managing Morrowind/OpenMW.
    """

    # Valid OpenMW-specific file extensions
    VALID_EXTENSIONS = (".omwaddon", ".omwscripts", ".omwgame")

    VALID_FOLDERS = ("animations", "fonts", "l10n", "mygui", "scripts", "shaders")

    def __init__(self, log: CommonLog):
        super().__init__()
        self._log = log

    def _hasValidContent(self, filetree: mobase.IFileTree) -> bool:
        """
        Check if tree contains valid OpenMW files.

        Args:
            filetree: The file tree to check.

        Returns:
            True if any valid OpenMW files are found.
        """
        for entry in filetree:
            name = entry.name().lower()
            if name.endswith(self.VALID_EXTENSIONS):
                return True
            
        for entry in filetree:
            if entry.isDir() and entry.name().lower() in self.VALID_FOLDERS:
                return True
        return False

    def dataLooksValid(
        self, filetree: mobase.IFileTree
    ) -> "mobase.ModDataChecker.CheckReturn":
        """
        Check if the mod contains valid OpenMW content files.

        Args:
            filetree: The file tree representing the mod's directory structure.

        Returns:
            VALID if omwaddon/omwscripts/omwgame files exist.
            INVALID if none found (allows other checkers to validate).
        """
        if self._hasValidContent(filetree):
            self._log.debug("Found valid OpenMW content files")
            return mobase.ModDataChecker.VALID

        # Return INVALID to let other checkers validate
        return mobase.ModDataChecker.INVALID

    def fix(self, filetree: mobase.IFileTree) -> mobase.IFileTree:
        """
        Fix the mod structure if needed.

        OpenMW files are already correctly structured, so no fixing is needed.

        Args:
            filetree: The file tree to fix.

        Returns:
            The unmodified file tree.
        """
        return filetree
