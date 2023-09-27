import mobase
from ...shared.shared_settings import SharedSettings

class ModdySettings(SharedSettings):
    """ Moddy settings module. Used to load various plugin settings. """

    def __init__(self, organiser = mobase.IOrganizer):
        super().__init__("Moddy", organiser)
        
    def disabledchecks(self):
        """ Lists the checks to skip. """
        setting = self.setting("disabledchecks")
        if setting:
            return setting.split("|")
        else:
            return []
    
    def notificationchecks(self):
        """ Lists the checks to only show notifications for. """
        setting = self.setting("notificationchecks")
        if setting:
            return setting.split("|")
        else:
            return []

    def messagelevel(self):
        """ The threshold to start showing messages. """
        return self.setting("messagelevel")
    
    def notificationsonly(self):
        """ If enabled, only show regular notifications and don't have Moddy pop up otherwise. """
        return self.setting("notificationsonly")