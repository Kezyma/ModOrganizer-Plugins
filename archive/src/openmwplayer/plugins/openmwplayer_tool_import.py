try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
from ..openmwplayer_plugin import OpenMWPlayerPlugin
import mobase

class OpenMWPlayerImportTool(OpenMWPlayerPlugin, mobase.IPluginTool):
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
        return self.baseName() + " Import Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Import"

    def description(self):
        return self.__tr("Imports the current settings from OpenMW.")

    def display(self):
        if self.openMWPlayer.paths.hasOpenMwCfg():
            self.openMWPlayer.newImportOpenMwCfg()
            self.openMWPlayer.newImportSettingsCfg()
