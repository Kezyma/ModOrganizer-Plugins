import mobase, os
from pathlib import Path
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from .openmwplayer_strings import OpenMWPlayerStrings
from ....common.common_qt import *
from ....common.common_utilities import *

class OpenMWPlayerDeploy():
    """ OpenMW Player deploy module, handles deploying openmw.cfg and settings.cfg when running OpenMW."""

    def __init__(self, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings, strings:OpenMWPlayerStrings):
        self._organiser = organiser
        self._settings = settings
        self._strings = strings


