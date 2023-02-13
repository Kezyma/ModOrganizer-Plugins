import mobase
from ...shared.shared_settings import SharedSettings

class OpenMWPlayerSettings(SharedSettings):
    """ OpenMW Player settings module. Used to load various plugin settings. """

    def __init__(self, organiser = mobase.IOrganizer):
        super().__init__("OpenMWPlayer", organiser)

    def cfgpath(self):
        """ The path to the openmw.cfg to be used. """
        return self.setting("openmwcfgpath")