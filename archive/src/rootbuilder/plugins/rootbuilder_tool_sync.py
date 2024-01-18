try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
from ..rootbuilder_plugin import RootBuilderPlugin
import mobase

class RootBuilderSyncTool(RootBuilderPlugin, mobase.IPluginTool):
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
        return self.icons.syncIcon()

    def name(self):
        return self.baseName() + " Sync Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Sync"

    def description(self):
        return self.__tr("Runs a sync operation using current settings.")

    def display(self):
        self.rootBuilder.sync()
