import mobase
from ....base.base_settings import BaseSettings

class ShortcutterSettings(BaseSettings):
    """ Shortcutter settings module. Used to load various plugin settings. """

    def __init__(self, organiser:mobase.IOrganizer):
        super().__init__("Shortcutter", organiser)