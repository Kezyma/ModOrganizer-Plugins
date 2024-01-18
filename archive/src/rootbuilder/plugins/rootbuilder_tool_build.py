try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
from ..rootbuilder_plugin import RootBuilderPlugin
import mobase

class RootBuilderBuildTool(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []

    def icon(self):
        return self.icons.plusIcon()

    def name(self):
        return self.baseName() + " Build Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Build"

    def description(self):
        return self.__tr("Runs a build operation using the current settings.")

    def display(self):
        self.rootBuilder.build()
