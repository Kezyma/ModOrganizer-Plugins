import mobase
from pathlib import Path
from functools import cached_property
from ....common.common_strings import CommonStrings

class ShortcutterStrings(CommonStrings):
    """Shortcutter strings module, contains strings used by Root Builder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

    @cached_property
    def scUpdateFilePath(self) -> str:
        """Gets the path to the file used for checking Root Builder updates."""
        return str(Path(self.pluginDataPath, "VersionManifest.json"))
