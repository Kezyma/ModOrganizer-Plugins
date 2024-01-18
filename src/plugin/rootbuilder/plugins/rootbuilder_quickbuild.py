from ..core.rootbuilder_plugin import RootBuilderPlugin
from ....common.common_qt import *
from ....common.common_icons import PLUS_ICON
import mobase

class RootBuilderQuickBuild(RootBuilderPlugin, mobase.IPluginTool):
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
        return PLUS_ICON

    def name(self):
        return f"{self.baseName()} Build Tool"

    def displayName(self):
        return f"{self.baseDisplayName()}/Build"

    def description(self):
        return self.__tr("Runs a build operation using the current settings.")

    def display(self):
        self._rootBuilder.build()