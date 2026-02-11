import mobase
from ..core.openmwplayer_plugin import OpenMWPlayerPlugin
from ....common.common_qt import *


class OpenMWPlayerMapper(OpenMWPlayerPlugin, mobase.IPluginFileMapper):
    """USVFS file mapper plugin for OpenMW Player."""

    def __init__(self):
        super().__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self.baseName()

    def settings(self):
        return []

    def name(self):
        return self.baseName() + " Mapper"

    def displayName(self):
        return self.baseDisplayName() + " Mapper"

    def description(self):
        return self.__tr("Provides USVFS file mappings for OpenMW configuration and saves.")

    def mappings(self):
        """Returns USVFS mappings for OpenMW Player."""
        return self._openmwPlayer._mappings.getMappings()
