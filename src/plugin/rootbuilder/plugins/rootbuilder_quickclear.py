from ..core.rootbuilder_plugin import RootBuilderPlugin
from ....common.common_qt import *
import mobase

class RootBuilderQuickClear(RootBuilderPlugin, mobase.IPluginTool):
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
        return self._icons.minusIcon()

    def name(self):
        return f"{self.baseName()} Clear Tool"

    def displayName(self):
        return f"{self.baseDisplayName()}/Clear"

    def description(self):
        return self.__tr("Runs a clear operation using current settings.")

    def display(self):
        self._rootBuilder.clear()