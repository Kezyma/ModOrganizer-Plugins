import mobase
from pathlib import Path
from functools import cached_property
from ....common.common_strings import CommonStrings

class ShortcutterStrings(CommonStrings):
    """Shortcutter strings module, contains strings used by Shortcutter."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)
