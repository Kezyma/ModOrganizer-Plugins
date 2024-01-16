import mobase
from ....base.base_plugin import BasePlugin
from .shortcutter import Shortcutter
try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication

class ShortcutterPlugin(BasePlugin):
    """Base Shortcutter plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("Shortcutter", "Shortcutter", mobase.VersionInfo(2, 0, 0))

    def init(self, organiser:mobase.IOrganizer):
        self._shortcutter = Shortcutter(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = []
        for setting in customSettings:
            baseSettings.append(setting)
        return baseSettings
        