import mobase
from ....base.base_settings import BaseSettings

class OpenMWPlayerSettings(BaseSettings):
    """ OpenMW Player settings module. Used to load various plugin settings. """

    def __init__(self, organiser:mobase.IOrganizer):
        super().__init__("OpenMWPlayer", organiser)

    def cfgpath(self):
        """ The path to the openmw.cfg to be used. """
        return self.setting("openmwcfgpath")

    def dummyesp(self):
        """ Whether to use dummy esp files to enable omwaddons. """
        return self.setting("dummyesp")

    def legacymode(self) -> bool:
        """ Whether to use legacy deployment mode (disabled by default). """
        return self.setting("legacymode")

    def openmwexepath(self) -> str:
        """ Path to openmw.exe for OpenMW folder mappings (auto-detected). """
        return self.setting("openmwexepath")