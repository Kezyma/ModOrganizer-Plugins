import mobase
from pathlib import Path
from ....common.common_qt import *
from ....common.common_log import CommonLog
from .listexporter_settings import ListExporterSettings
from ..modules.listexporter_html import ListExporterHtml
from ..modules.listexporter_json import ListExporterJson

class ListExporter:
    """Core List Exporter class that handles all plugin functionality."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = ListExporterSettings(self._organiser)
        self._log = CommonLog("ListExporter", self._settings)
        self._html = ListExporterHtml(organiser)
        self._json = ListExporterJson(organiser)

    def exportJson(self):
        manualPath = Path(QFileDialog.getSaveFileName(None, "Please select where modlist data should be exported.", ".", "JSON Files (*.json)")[0])
        self._json.export(manualPath)

    def exportHtml(self):
        manualPath = Path(QFileDialog.getSaveFileName(None, "Please select where modlist data should be exported.", ".", "HTML Files (*.html)")[0])
        self._html.export(manualPath)

