import mobase
from ....base.base_plugin import BasePlugin
from .listexporter import ListExporter
from ....common.common_qt import *

class ListExporterPlugin(BasePlugin):
    """Base List Exporter plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("ListExporter", "List Exporter", mobase.VersionInfo(0, 0, 1))

    def init(self, organiser:mobase.IOrganizer):
        self._listExporter = ListExporter(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("enabled", self.__tr(f"Enables {self._pluginName}"), True),
            mobase.PluginSetting("loglevel", self.__tr(f"Controls the logging for {self._pluginName}"), 1)
            ]
        for setting in customSettings:
            baseSettings.append(setting)
        return customSettings
        