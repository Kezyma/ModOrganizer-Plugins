import mobase
from ...shared.shared_paths import SharedPaths

class ShortcutterPaths(SharedPaths):
    """ Shortcutter path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("Shortcutter", organiser) 