import mobase
from pathlib import Path
from functools import cached_property
from ....common.common_strings import CommonStrings

class ReinstallerStrings(CommonStrings):
    """Reinstaller strings module, contains strings used by Reinstaller."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        super().__init__(plugin, organiser)

