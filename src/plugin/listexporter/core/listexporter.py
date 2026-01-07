import mobase
from typing import List
from ....common.common_log import CommonLog
from .listexporter_settings import ListExporterSettings
from ..modules.listexporter_strings import ListExporterStrings
from ..modules.listexporter_data import ListExporterData
from ..modules.listexporter_formats import ListExporterFormats


class ListExporter:
    """Core List Exporter class that handles all plugin functionality."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = ListExporterSettings(self._organiser)
        self._log = CommonLog("ListExporter", self._settings)
        self._strings = ListExporterStrings("ListExporter", organiser)
        self._data = ListExporterData(organiser, self._strings, self._log)
        self._formats = ListExporterFormats(organiser, self._log)

    def export(self, profiles: List[str], columns: List[str], format: str,
               separateCategories: bool, path: str) -> bool:
        """
        Export mod list to file.

        Args:
            profiles: List of profile names to include
            columns: List of column IDs to include
            format: Export format (markdown, html, csv, json)
            separateCategories: Whether to create separate tables per category
            path: Output file path

        Returns:
            True if export succeeded, False otherwise
        """
        self._log.info(f"Exporting {len(profiles)} profiles to {format} format")

        # Collect mod data
        mods, categories = self._data.collectModData(profiles)
        self._log.debug(f"Collected {len(mods)} mods in {len(categories)} categories")

        if not mods:
            self._log.warning("No mods to export")
            return False

        # Export based on format
        if format == "markdown":
            return self._formats.exportMarkdown(mods, categories, columns, profiles, separateCategories, path)
        elif format == "csv":
            return self._formats.exportCsv(mods, categories, columns, profiles, separateCategories, path)
        elif format == "json":
            return self._formats.exportJson(mods, categories, columns, profiles, separateCategories, path)
        else:  # html
            return self._formats.exportHtml(mods, categories, columns, profiles, separateCategories, path)
