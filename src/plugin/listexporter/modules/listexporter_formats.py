import csv
import os
from typing import List, Dict, Optional
from ..models.listexporter_modinfo import ModInfo
from ....common.common_log import CommonLog
from ....common.common_utilities import saveLines, saveJson


class ExportColumn:
    """Available export columns."""
    MOD = "mod"
    CATEGORY = "category"
    NOTES = "notes"
    COMMENTS = "comments"
    NEXUS_ID = "nexusid"
    NEXUS_URL = "nexusurl"
    # Profile columns are dynamic: "profile:{name}"


class ListExporterFormats:
    """Handles exporting mod data to various formats."""

    def __init__(self, organiser, log: CommonLog):
        self._organiser = organiser
        self._log = log

    def _getNexusGame(self, gameName: Optional[str]) -> str:
        """Gets Nexus game name for URL building."""
        if not gameName:
            gameName = self._organiser.managedGame().gameName()
        try:
            game = self._organiser.getGame(gameName)
            if game:
                return game.gameNexusName()
        except:
            pass
        return ""

    def _escapeForFormat(self, text: str, format: str) -> str:
        """Escape special characters for the given format."""
        if not text:
            return ""
        if format == "html":
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        elif format == "markdown":
            # Escape pipe characters which break table cells
            return text.replace("|", "\\|").replace("\n", " ")
        elif format == "csv":
            # CSV handles escaping via the csv module
            return text.replace("\n", " ")
        return text

    def _buildHeaders(self, columns: List[str], profiles: List[str], separateCategories: bool) -> List[str]:
        """Build column headers based on selected columns."""
        headers = []
        for col in columns:
            if col == ExportColumn.MOD:
                headers.append("Mod")
            elif col == ExportColumn.CATEGORY and not separateCategories:
                headers.append("Category")
            elif col == ExportColumn.NOTES:
                headers.append("Notes")
            elif col == ExportColumn.COMMENTS:
                headers.append("Comments")
            elif col == ExportColumn.NEXUS_ID:
                headers.append("Nexus ID")
            elif col == ExportColumn.NEXUS_URL:
                headers.append("Nexus URL")
            elif col.startswith("profile:"):
                profileName = col.replace("profile:", "")
                headers.append(profileName)
        return headers

    def _buildRow(self, mod: ModInfo, columns: List[str], profiles: List[str],
                  separateCategories: bool, format: str) -> List[str]:
        """Build a row of data for a mod."""
        row = []
        nexusGame = self._getNexusGame(mod.game_name)

        for col in columns:
            if col == ExportColumn.MOD:
                nexusUrl = mod.nexus_url(nexusGame)
                if format == "html" and nexusUrl:
                    escapedName = self._escapeForFormat(mod.name, format)
                    row.append(f"<a href='{nexusUrl}' target='_blank'>{escapedName}</a>")
                elif format == "markdown" and nexusUrl:
                    escapedName = self._escapeForFormat(mod.name, format)
                    row.append(f"[{escapedName}]({nexusUrl})")
                else:
                    row.append(self._escapeForFormat(mod.name, format))
            elif col == ExportColumn.CATEGORY and not separateCategories:
                row.append(self._escapeForFormat(mod.category, format))
            elif col == ExportColumn.NOTES:
                row.append(self._escapeForFormat(mod.notes, format))
            elif col == ExportColumn.COMMENTS:
                row.append(self._escapeForFormat(mod.comments, format))
            elif col == ExportColumn.NEXUS_ID:
                row.append(str(mod.nexus_id) if mod.nexus_id and mod.nexus_id > 0 else "")
            elif col == ExportColumn.NEXUS_URL:
                nexusUrl = mod.nexus_url(nexusGame)
                row.append(nexusUrl if nexusUrl else "")
            elif col.startswith("profile:"):
                profileName = col.replace("profile:", "")
                enabled = mod.enabled_profiles.get(profileName, False)
                if format == "html":
                    row.append("&#10003;" if enabled else "&#10007;")
                elif format == "markdown":
                    row.append("✓" if enabled else "✗")
                elif format == "json":
                    row.append(enabled)
                else:  # csv
                    row.append("Yes" if enabled else "No")
        return row

    def _groupByCategory(self, mods: List[ModInfo]) -> Dict[str, List[ModInfo]]:
        """Group mods by category, with uncategorized mods in a separate group."""
        byCategory = {}
        for mod in mods:
            cat = mod.category if mod.category else "Uncategorized"
            if cat not in byCategory:
                byCategory[cat] = []
            byCategory[cat].append(mod)
        return byCategory

    def exportMarkdown(self, mods: List[ModInfo], categories: List[str],
                       columns: List[str], profiles: List[str],
                       separateCategories: bool, path: str) -> bool:
        """Export to Markdown format."""
        lines = []
        headers = self._buildHeaders(columns, profiles, separateCategories)

        if separateCategories:
            byCategory = self._groupByCategory(mods)

            # Export each category in order
            for category in categories:
                if category in byCategory:
                    lines.append(f"\n## {category}\n\n")
                    lines.append("| " + " | ".join(headers) + " |\n")
                    lines.append("| " + " | ".join(["---"] * len(headers)) + " |\n")
                    for mod in byCategory[category]:
                        row = self._buildRow(mod, columns, profiles, separateCategories, "markdown")
                        lines.append("| " + " | ".join(str(c) for c in row) + " |\n")

            # Handle uncategorized mods
            if "Uncategorized" in byCategory:
                lines.append(f"\n## Uncategorized\n\n")
                lines.append("| " + " | ".join(headers) + " |\n")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |\n")
                for mod in byCategory["Uncategorized"]:
                    row = self._buildRow(mod, columns, profiles, separateCategories, "markdown")
                    lines.append("| " + " | ".join(str(c) for c in row) + " |\n")
        else:
            lines.append("| " + " | ".join(headers) + " |\n")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |\n")
            for mod in mods:
                row = self._buildRow(mod, columns, profiles, separateCategories, "markdown")
                lines.append("| " + " | ".join(str(c) for c in row) + " |\n")

        return saveLines(path, lines)

    def exportCsv(self, mods: List[ModInfo], categories: List[str],
                  columns: List[str], profiles: List[str],
                  separateCategories: bool, path: str) -> bool:
        """Export to CSV format."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                headers = self._buildHeaders(columns, profiles, separateCategories)

                if separateCategories:
                    byCategory = self._groupByCategory(mods)

                    # Get categories to iterate (include Uncategorized if present)
                    allCategories = list(categories)
                    if "Uncategorized" in byCategory and "Uncategorized" not in allCategories:
                        allCategories.append("Uncategorized")

                    for category in allCategories:
                        if category in byCategory:
                            writer.writerow([f"=== {category} ==="])
                            writer.writerow(headers)
                            for mod in byCategory[category]:
                                row = self._buildRow(mod, columns, profiles, separateCategories, "csv")
                                writer.writerow(row)
                            writer.writerow([])  # Empty row between sections
                else:
                    writer.writerow(headers)
                    for mod in mods:
                        row = self._buildRow(mod, columns, profiles, separateCategories, "csv")
                        writer.writerow(row)
            return True
        except Exception as e:
            self._log.warning(f"Error exporting CSV: {e}")
            return False

    def exportJson(self, mods: List[ModInfo], categories: List[str],
                   columns: List[str], profiles: List[str],
                   separateCategories: bool, path: str) -> bool:
        """Export to JSON format."""
        def modToDict(mod: ModInfo) -> Dict:
            result = {}
            nexusGame = self._getNexusGame(mod.game_name)

            for col in columns:
                if col == ExportColumn.MOD:
                    result["mod"] = mod.name
                    if mod.nexus_id and mod.nexus_id > 0:
                        url = mod.nexus_url(nexusGame)
                        if url:
                            result["nexusUrl"] = url
                        result["nexusId"] = mod.nexus_id
                elif col == ExportColumn.CATEGORY and not separateCategories:
                    result["category"] = mod.category
                elif col == ExportColumn.NOTES:
                    result["notes"] = mod.notes
                elif col == ExportColumn.COMMENTS:
                    result["comments"] = mod.comments
                elif col.startswith("profile:"):
                    profileName = col.replace("profile:", "")
                    if "profiles" not in result:
                        result["profiles"] = {}
                    result["profiles"][profileName] = mod.enabled_profiles.get(profileName, False)
            return result

        if separateCategories:
            data = {}
            byCategory = self._groupByCategory(mods)

            # Export categories in order
            for category in categories:
                if category in byCategory:
                    data[category] = [modToDict(mod) for mod in byCategory[category]]

            # Handle uncategorized
            if "Uncategorized" in byCategory:
                data["Uncategorized"] = [modToDict(mod) for mod in byCategory["Uncategorized"]]
        else:
            data = [modToDict(mod) for mod in mods]

        return saveJson(path, data)

    def exportHtml(self, mods: List[ModInfo], categories: List[str],
                   columns: List[str], profiles: List[str],
                   separateCategories: bool, path: str) -> bool:
        """Export to HTML format with Bootstrap styling."""
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("<meta charset='utf-8'>")
        html.append("<meta name='viewport' content='width=device-width, initial-scale=1'>")
        html.append("<title>Mod List Export</title>")
        html.append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'>")
        html.append("<style>")
        html.append(".check { color: green; font-weight: bold; }")
        html.append(".cross { color: red; }")
        html.append("</style>")
        html.append("</head>")
        html.append("<body class='bg-secondary'>")
        html.append("<div class='container py-3'>")

        headers = self._buildHeaders(columns, profiles, separateCategories)

        def writeTable(modList: List[ModInfo], title: Optional[str] = None):
            if title:
                html.append(f"<h3 class='text-white mt-4'>{self._escapeForFormat(title, 'html')}</h3>")
            html.append("<div class='card mb-3'>")
            html.append("<div class='card-body p-0'>")
            html.append("<table class='table table-sm table-striped mb-0'>")
            html.append("<thead>")
            html.append("<tr>")
            for h in headers:
                html.append(f"<th>{self._escapeForFormat(h, 'html')}</th>")
            html.append("</tr>")
            html.append("</thead>")
            html.append("<tbody>")
            for mod in modList:
                html.append("<tr>")
                row = self._buildRow(mod, columns, profiles, separateCategories, "html")
                for cell in row:
                    cellStr = str(cell)
                    # Style check/cross marks
                    if "&#10003;" in cellStr:
                        html.append(f"<td class='check'>{cellStr}</td>")
                    elif "&#10007;" in cellStr:
                        html.append(f"<td class='cross'>{cellStr}</td>")
                    else:
                        html.append(f"<td>{cellStr}</td>")
                html.append("</tr>")
            html.append("</tbody>")
            html.append("</table>")
            html.append("</div>")
            html.append("</div>")

        if separateCategories:
            byCategory = self._groupByCategory(mods)

            for category in categories:
                if category in byCategory:
                    writeTable(byCategory[category], category)

            if "Uncategorized" in byCategory:
                writeTable(byCategory["Uncategorized"], "Uncategorized")
        else:
            writeTable(mods)

        html.append("</div>")
        html.append("</body>")
        html.append("</html>")

        return saveLines(path, ["\n".join(html)])
