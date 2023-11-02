from ..core.rootbuilder_plugin import RootBuilderPlugin
from ....common.common_qt import *
from ....common.common_icons import SYNC_ICON
import mobase

class RootBuilderQuickSync(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser: mobase.IOrganizer):
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
        return f"{self.baseName()} Sync Tool"

    def displayName(self):
        return f"{self.baseDisplayName()}/Sync"

    def description(self):
        return self.__tr("Runs a sync operation using current settings.")

    def display(self):
        self._rootBuilder.sync()