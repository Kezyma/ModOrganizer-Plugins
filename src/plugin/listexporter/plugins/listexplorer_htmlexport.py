import mobase
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *
from ..core.listexporter_plugin import ListExporterPlugin

class ListExplorerHtmlExport(ListExporterPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return DOWNLOAD_ICON

    def name(self):
        return self.baseName() + " (HTML)"

    def displayName(self):
        return self.baseDisplayName() + "/Export Html"

    def description(self):
        return self.__tr("Exports the current mod list as HTML.")
    
    def display(self):
        self._listExporter.exportHtml()


