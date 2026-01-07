import mobase
from ....common.common_log import CommonLog


class RootBuilderDataChecker(mobase.ModDataChecker):
    """
    ModDataChecker GameFeature that validates 'Root' as a valid mod folder.

    This is not a plugin - it's a GameFeature that gets registered by
    RootBuilderAutobuild during initialization. When MO2 checks if a mod
    has valid structure, this checker returns VALID for mods containing
    a 'Root' folder at the top level.

    This prevents MO2 from showing "mod structure looks incorrect" warnings
    for mods that are structured for Root Builder.
    """

    def __init__(self, log: CommonLog):
        super().__init__()
        self._log = log

    def dataLooksValid(
        self, filetree: mobase.IFileTree
    ) -> mobase.ModDataChecker.CheckReturn:
        """
        Check if the mod contains a Root folder.

        Args:
            filetree: The file tree representing the mod's directory structure.

        Returns:
            VALID if a 'Root' folder exists at the top level.
            INVALID if no Root folder found (allows other checkers to validate).
        """
        for entry in filetree:
            if entry.isDir() and entry.name().lower() == "root":
                self._log.debug(f"Found valid Root folder in mod")
                return mobase.ModDataChecker.VALID

        # Return INVALID to let other checkers validate
        # (INVALID means "I don't recognize this structure", not "this is bad")
        return mobase.ModDataChecker.INVALID

    def fix(self, filetree: mobase.IFileTree) -> mobase.IFileTree:
        """
        Fix the mod structure if needed.

        Root folders are already correctly structured, so no fixing is needed.

        Args:
            filetree: The file tree to fix.

        Returns:
            The unmodified file tree.
        """
        return filetree
