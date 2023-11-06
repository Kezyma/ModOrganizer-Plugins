import mobase
from ....base.base_plugin import BasePlugin
from .pluginfinder import PluginFinder
from ....common.common_qt import *

class PluginFinderPlugin(BasePlugin):
    """Base Plugin Finder plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("PluginFinder", "Plugin Finder", mobase.VersionInfo(2, 0, 0, mobase.ReleaseType.FINAL))

    def init(self, organiser:mobase.IOrganizer):
        self._pluginFinder = PluginFinder(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("enabled", self.__tr(f"Enables {self._pluginName}"), True),
            mobase.PluginSetting("loglevel", self.__tr(f"Controls the logging for {self._pluginName}"), 1),
            mobase.PluginSetting("priority", self.__tr("The priority of the installer module for installing plugins."), 120)
            ]
        for setting in customSettings:
            baseSettings.append(setting)
        return customSettings
        