import mobase
from ...shared.shared_settings import SharedSettings

class ModdySettings(SharedSettings):
    """ Moddy settings module. Used to load various plugin settings. """

    def __init__(self, organiser = mobase.IOrganizer):
        super().__init__("Moddy", organiser)
        
    def disabledchecks(self):
        """ Lists the checks to skip. """
        return self.setting("disabledchecks")
    
    def messagelevel(self):
        """ The threshold to start showing messages. """
        return self.setting("messagelevel")