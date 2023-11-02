import mobase
from ....base.base_settings import BaseSettings

class PluginFinderSettings(BaseSettings):
    """ Plugin Finder settings module. Used to load various plugin settings. """

    def __init__(self, organiser:mobase.IOrganizer):
        super().__init__("PluginFinder", organiser)