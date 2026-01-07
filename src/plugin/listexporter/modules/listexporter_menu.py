import mobase
from pathlib import Path

try:
    from ..ui.qt6.listexporter_menu import Ui_ListExporterMenu
    from ....base.ui.qt6.update_widget import Ui_updateTabWidget
    from PyQt6.QtWidgets import QMessageBox, QAbstractItemView
    from PyQt6 import QtCore as QtCoreLocal
    qUserRole = QtCoreLocal.Qt.ItemDataRole.UserRole
    qDropAction = QtCoreLocal.Qt.DropAction.MoveAction
    qDragDropMode = QAbstractItemView.DragDropMode.InternalMove
except:
    from ..ui.qt5.listexporter_menu import Ui_ListExporterMenu
    from ....base.ui.qt5.update_widget import Ui_updateTabWidget
    from PyQt5.QtWidgets import QMessageBox, QAbstractItemView
    from PyQt5 import QtCore as QtCoreLocal
    qUserRole = QtCoreLocal.Qt.UserRole
    qDropAction = QtCoreLocal.Qt.MoveAction
    qDragDropMode = QAbstractItemView.InternalMove

from ..core.listexporter import ListExporter
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ....common.common_icons import *
from ....common.common_qt import *


class ListExporterMenu(QtWidgets.QWidget):
    """List Exporter main menu widget."""

    def __init__(self, parent: QtWidgets.QWidget, organiser: mobase.IOrganizer,
                 listExporter: ListExporter, update: CommonUpdate, help: CommonHelp):
        super().__init__(parent)
        self._organiser = organiser
        self._listExporter = listExporter
        self._update = update
        self._help = help
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_ListExporterMenu()
        self.widget.setupUi(self)

        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)
        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self._update.configure(self.updateTabWidget)
        self._help.configure(self.helpTabWidget)

        # Connect signals
        self.widget.btnSelectAll.clicked.connect(self.selectAllProfiles)
        self.widget.btnSelectNone.clicked.connect(self.selectNoProfiles)
        self.widget.btnExport.clicked.connect(self.doExport)
        self.widget.lstProfiles.itemChanged.connect(self.updateColumnList)
        self.widget.chkSeparateCategories.stateChanged.connect(self.updateColumnList)

        # Set icons
        self.widget.btnExport.setIcon(DOWNLOAD_ICON)

        # Enable drag-drop reordering for column list
        self.widget.lstColumns.setDragDropMode(qDragDropMode)
        self.widget.lstColumns.setDefaultDropAction(qDropAction)

    def rebind(self):
        """Rebinds the UI with current data."""
        self.bindProfileList()
        self.bindColumnList()

    def bindProfileList(self):
        """Populates the profile list."""
        self.widget.lstProfiles.clear()
        profiles = self._listExporter._data.getProfileList()
        currentProfile = self._organiser.profile().name()

        for profile in sorted(profiles):
            item = QtWidgets.QListWidgetItem()
            item.setText(profile)
            item.setFlags(item.flags() | qItemFlag.ItemIsUserCheckable)
            item.setCheckState(qCheckState.Checked if profile == currentProfile else qCheckState.Unchecked)
            self.widget.lstProfiles.addItem(item)

    def bindColumnList(self):
        """Populates the column selection list."""
        # Block signals to prevent recursive updates
        self.widget.lstColumns.blockSignals(True)
        self.widget.lstColumns.clear()
        separateCategories = self.widget.chkSeparateCategories.isChecked()

        # Static columns
        columns = [
            ("mod", "Mod Name", True),
            ("notes", "Notes", True),
            ("comments", "Comments", True),
        ]

        # Category column only if not separating
        if not separateCategories:
            columns.insert(1, ("category", "Category", True))

        # Add profile columns for selected profiles
        selectedProfiles = self.getSelectedProfiles()
        if len(selectedProfiles) > 1:
            for profile in selectedProfiles:
                columns.append((f"profile:{profile}", f"Profile: {profile}", True))

        for colId, colName, checked in columns:
            item = QtWidgets.QListWidgetItem()
            item.setText(colName)
            item.setData(qUserRole, colId)
            item.setFlags(item.flags() | qItemFlag.ItemIsUserCheckable | qItemFlag.ItemIsDragEnabled)
            item.setCheckState(qCheckState.Checked if checked else qCheckState.Unchecked)
            self.widget.lstColumns.addItem(item)

        self.widget.lstColumns.blockSignals(False)

    def updateColumnList(self):
        """Updates column list when profile selection or options change."""
        self.bindColumnList()

    def selectAllProfiles(self):
        """Selects all profiles."""
        for i in range(self.widget.lstProfiles.count()):
            self.widget.lstProfiles.item(i).setCheckState(qCheckState.Checked)

    def selectNoProfiles(self):
        """Deselects all profiles."""
        for i in range(self.widget.lstProfiles.count()):
            self.widget.lstProfiles.item(i).setCheckState(qCheckState.Unchecked)

    def getSelectedProfiles(self) -> list:
        """Returns list of selected profile names."""
        profiles = []
        for i in range(self.widget.lstProfiles.count()):
            item = self.widget.lstProfiles.item(i)
            if item.checkState() == qCheckState.Checked:
                profiles.append(item.text())
        return profiles

    def getSelectedColumns(self) -> list:
        """Returns list of selected column IDs."""
        columns = []
        for i in range(self.widget.lstColumns.count()):
            item = self.widget.lstColumns.item(i)
            if item.checkState() == qCheckState.Checked:
                columns.append(item.data(qUserRole))
        return columns

    def getSelectedFormat(self) -> str:
        """Returns selected export format."""
        if self.widget.rbMarkdown.isChecked():
            return "markdown"
        elif self.widget.rbCsv.isChecked():
            return "csv"
        elif self.widget.rbJson.isChecked():
            return "json"
        return "html"

    def doExport(self):
        """Performs the export."""
        profiles = self.getSelectedProfiles()
        if not profiles:
            QMessageBox.warning(self, "No Profiles", "Please select at least one profile.")
            return

        columns = self.getSelectedColumns()
        if not columns:
            QMessageBox.warning(self, "No Columns", "Please select at least one column.")
            return

        format = self.getSelectedFormat()
        separateCategories = self.widget.chkSeparateCategories.isChecked()

        # Get file path
        extensions = {
            "markdown": ("Markdown Files (*.md)", ".md"),
            "html": ("HTML Files (*.html)", ".html"),
            "csv": ("CSV Files (*.csv)", ".csv"),
            "json": ("JSON Files (*.json)", ".json")
        }

        filterStr, defaultExt = extensions[format]
        path = QFileDialog.getSaveFileName(
            self,
            "Export Mod List",
            f"modlist{defaultExt}",
            filterStr
        )[0]

        if not path:
            return

        # Collect data and export
        success = self._listExporter.export(
            profiles=profiles,
            columns=columns,
            format=format,
            separateCategories=separateCategories,
            path=path
        )

        if success:
            QMessageBox.information(self, "Export Complete", f"Mod list exported to:\n{path}")
        else:
            QMessageBox.warning(self, "Export Failed", "Failed to export mod list. Check the log for details.")
