from ..core.openmwplayer_plugin import OpenMWPlayerPlugin
from ....common.common_qt import *
from ....common.common_icons import *
import mobase

class OpenMWPlayerQuickExport(OpenMWPlayerPlugin, mobase.IPluginTool):
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
        return LINK_ICON

    def name(self):
        return self.baseName() + " Export Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Export"

    def description(self):
        return self.__tr("Exports the current settings to OpenMW.")

    def display(self):
        self._openmwPlayer._import.exportOpenmwCfg()
        self._openmwPlayer._import.exportSettingsCfg()
