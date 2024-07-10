import mobase
from ....base.base_settings import BaseSettings

class ProfileSyncSettings(BaseSettings):
    """ Profile Sync settings module. Used to load various plugin settings. """

    def __init__(self, organiser:mobase.IOrganizer):
        super().__init__("ProfileSync", organiser)

    def useasync(self):
        """ Determines whether to use threads for saving functions. """
        return self.setting("useasync")