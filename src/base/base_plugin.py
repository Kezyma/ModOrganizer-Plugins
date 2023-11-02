try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication

from .base_settings import BaseSettings
from ..common.common_icons import MENU_ICON
from ..common.common_log import CommonLog

import mobase

class BasePlugin():
    """ Base class for all plugins to inherit from and overwrite. """

    def __init__(self, pluginName : str, displayName : str, version : mobase.VersionInfo):
        self._pluginName = pluginName
        self._displayName = displayName
        self._pluginVersion = version
        super().__init__()

    def init(self, organiser = mobase.IOrganizer):
        self._organiser = organiser
        self._baseSettings = BaseSettings(self._pluginName, self._organiser)
        self._log = CommonLog(self._pluginName, self._organiser, self._baseSettings)
        return True

    def version(self):
        return self._pluginVersion

    def isActive(self):
        return self._baseSettings.enabled()

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def tr(self, trstr):
        return self.__tr(trstr)

    def icon(self):
        return MENU_ICON

    def author(self):
        return "Kezyma"

    def baseName(self):
        return self._pluginName

    def baseDisplayName(self):
        return self._displayName

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Plugin description. Overwrite me.")

    def tooltip(self):
        return self.description()

    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("enabled", f"Enables {self._pluginName}", True),
            mobase.PluginSetting("loglevel", f"Controls the logging for {self._pluginName}", 1)
            ]