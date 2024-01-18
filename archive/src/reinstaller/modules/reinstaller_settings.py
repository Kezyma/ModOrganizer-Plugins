import mobase
from ...shared.shared_settings import SharedSettings

class ReinstallerSettings(SharedSettings):
    """ Reinstaller settings module. Used to load various plugin settings. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("Reinstaller", organiser)

        

