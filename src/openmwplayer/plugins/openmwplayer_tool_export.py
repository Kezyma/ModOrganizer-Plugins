try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
from ..openmwplayer_plugin import OpenMWPlayerPlugin
import mobase

class OpenMWPlayerExportTool(OpenMWPlayerPlugin, mobase.IPluginTool):
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
        return self.icons.linkIcon()

    def name(self):
        return self.baseName() + " Export Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Export"

    def description(self):
        return self.__tr("Exports the current settings to OpenMW.")

    def display(self):
        self.openMWPlayer.newExportOpenMwCfg()
        self.openMWPlayer.newExportSettingsCfg()
