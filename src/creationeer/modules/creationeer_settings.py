import mobase
from ...shared.shared_settings import SharedSettings

class CreationeerSettings(SharedSettings):
    """ Creationeer settings module. Used to load various plugin settings. """

    def __init__(self, organiser = mobase.IOrganizer):
        super().__init__("Creationeer", organiser)

    def rootBuilderSupport(self):
        """ Whether to create and search Root mod folders. """
        return self.setting("rootbuildersupport")

    def modNameFormat(self):
        """ Format for creating mods. """
        return self.setting("modnameformat")

