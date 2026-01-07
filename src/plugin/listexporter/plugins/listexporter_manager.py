import mobase
from pathlib import Path
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ..core.listexporter_plugin import ListExporterPlugin
from ..modules.listexporter_menu import ListExporterMenu


class ListExporterManager(ListExporterPlugin, mobase.IPluginTool):
    """Main List Exporter manager plugin with dialog interface."""

    def __init__(self):
        super().__init__()

    def init(self, organiser: mobase.IOrganizer):
        res = super().init(organiser)
        self._update = CommonUpdate(
            "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/listexporter.json",
            "https://github.com/Kezyma/ModOrganizer-Plugins/releases",
            self,
            self._listExporter._strings,
            self._listExporter._log
        )
        self._help = CommonHelp(
            Path(__file__).parent.parent / "data" / "listexporter_help.html",
            "listexporter",
            "",
            "",
            self._listExporter._strings,
            self._listExporter._log
        )
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return DOWNLOAD_ICON

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Exports mod lists to various formats (HTML, Markdown, CSV, JSON).")

    def display(self):
        """Shows the export dialog."""
        dialog = BaseDialog(
            self.baseDisplayName(),
            str(self.version()),
            self.icon()
        )
        menu = ListExporterMenu(
            dialog,
            self._organiser,
            self._listExporter,
            self._update,
            self._help
        )
        menu.rebind()
        dialog.addContent(menu)
        dialog.exec()
