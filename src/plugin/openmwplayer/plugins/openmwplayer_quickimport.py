from ..core.openmwplayer_plugin import OpenMWPlayerPlugin
from ....common.common_qt import *
from ....common.common_icons import *
import mobase

class OpenMWPlayerQuickImport(OpenMWPlayerPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self._pluginName

    def settings(self):
        return []

    def icon(self):
        return SYNC_ICON

    def name(self):
        return self.baseName() + " Import Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Import"

    def description(self):
        return self.__tr("Imports the current settings from OpenMW.")

    def display(self):
        self._openmwPlayer.importSettings()
