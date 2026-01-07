import mobase
from ....base.base_plugin import BasePlugin
from .listexporter import ListExporter
from ....common.common_qt import *


class ListExporterPlugin(BasePlugin):
    """Base List Exporter plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("ListExporter", "List Exporter", mobase.VersionInfo(2, 0, 0))

    def init(self, organiser: mobase.IOrganizer):
        self._listExporter = ListExporter(organiser)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def settings(self):
        """Plugin settings for Mod Organizer."""
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("defaultformat", self.__tr("Default export format"), "html"),
            mobase.PluginSetting("separatecategories", self.__tr("Separate tables by category by default"), False),
        ]
        for setting in customSettings:
            baseSettings.append(setting)
        return baseSettings
