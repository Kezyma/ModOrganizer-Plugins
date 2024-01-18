import mobase
from ...shared.shared_settings import SharedSettings

class CurationClubSettings(SharedSettings):
    """ Curation Club settings module. Used to load various plugin settings. """

    def __init__(self, organiser = mobase.IOrganizer):
        super().__init__("CurationClub", organiser)

    def rootBuilderSupport(self):
        """ Whether to create and search Root mod folders. """
        return self.setting("rootbuildersupport")

    def modNameFormat(self):
        """ Format for creating mods. """
        return self.setting("modnameformat")

