import mobase, os
from pathlib import Path
from functools import cached_property
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from ....common.common_strings import CommonStrings
from ....common.common_qt import *

class OpenMWPlayerStrings(CommonStrings):
    """ OpenMW Player strings module, contains strings used by OpenMW Player. """

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings):
        self.settings = settings
        super().__init__(plugin, organiser) 
