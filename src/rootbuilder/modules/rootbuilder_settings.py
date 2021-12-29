import mobase
from ...shared.shared_settings import SharedSettings

class RootBuilderSettings(SharedSettings):
    """ Root Builder settings module. Used to load various plugin settings. """

    def __init__(self, organiser = mobase.IOrganizer):
        super().__init__("RootBuilder", organiser)

    def cache(self):
        """ Determines whether to cache game file hashes. """
        return self.setting("cache")

    def backup(self):
        """ Determines whether to take a full game backup. """
        return self.setting("backup")

    def autobuild(self):
        """ Determines whether to build automatically on run. """
        return self.setting("autobuild")

    def linkmode(self):
        """ Determines whether to use file linking. """
        return self.setting("linkmode")

    def usvfsmode(self):
        """ Determines whether to use usvfs root mapping. """
        return self.setting("usvfsmode")

    def linkextensions(self):
        """ Extensions to be linked if link mode is enabled. """
        return self.setting("linkextensions").split(",")

    def exclusions(self):
        """ Files to be excluded from all operations. """
        return self.setting("exclusions").split(",")

    def redirect(self):
        """ Whether to redirect apps launched from mod root folders. """
        return self.setting("redirect")

    def installer(self):
        """ Enables the installer plugin. """
        return self.setting("installer")

    def priority(self):
        """ The priority of the installer module for installing root mods. """
        return self.setting("priority")