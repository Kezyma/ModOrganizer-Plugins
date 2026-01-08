"""Curation Club manager plugin - main tool interface."""

import mobase
from pathlib import Path
from typing import List, Dict

from ..core.curationclub_plugin import CurationClubPlugin
from ..core.curationclub import CurationClub
from ..core.curationclub_settings import CurationClubSettings
from ..modules.curationclub_strings import CurationClubStrings
from ..models.curationclub_creationdata import (
    CreationData, createCreationData,
    CREATION_ID, CREATION_NAME, CREATION_FILES, CREATION_DESCRIPTION, CREATION_MANUAL
)
from ....common.common_qt import *
from ....common.common_icons import MENU_ICON
from ....common.common_log import CommonLog


class CurationClubManager(CurationClubPlugin, mobase.IPluginTool):
    """Main Curation Club manager tool."""

    def __init__(self):
        super().__init__()

    def init(self, organiser: mobase.IOrganizer) -> bool:
        res = super().init(organiser)
        self._curationclub = CurationClub(self._organiser)
        self._strings = CurationClubStrings("CurationClub", self._organiser)
        self._log = CommonLog("CurationClub", self._settings)
        self._strings.initializeDatabase()
        return res

    def name(self) -> str:
        return "CurationClubManager"

    def displayName(self) -> str:
        return "Curation Club"

    def tooltip(self) -> str:
        return self.tr("Manage Creation Club content")

    def icon(self) -> QIcon:
        return MENU_ICON

    def display(self):
        """Shows the main Curation Club dialog."""
        self._dialog = self._createDialog()
        self._dialog.exec()

    def _createDialog(self) -> QDialog:
        """Creates the main dialog."""
        dialog = QDialog()
        dialog.setWindowTitle("Curation Club")
        dialog.setWindowIcon(MENU_ICON)
        dialog.setMinimumSize(700, 500)

        layout = QVBoxLayout(dialog)

        # Create tab widget
        tabWidget = QTabWidget()

        # Curate tab
        curateTab = self._createCurateTab()
        tabWidget.addTab(curateTab, "Curate")

        # Editor tab
        editorTab = self._createEditorTab()
        tabWidget.addTab(editorTab, "Manual Editor")

        # Settings tab
        settingsTab = self._createSettingsTab()
        tabWidget.addTab(settingsTab, "Settings")

        layout.addWidget(tabWidget)

        return dialog

    def _createCurateTab(self) -> QWidget:
        """Creates the main curation tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Description
        descLabel = QLabel(
            "Scan your game folder for Creation Club content and organize it into MO2 mods.\n"
            "This allows you to manage CC content like regular mods."
        )
        descLabel.setWordWrap(True)
        layout.addWidget(descLabel)

        # Splitter for lists
        splitter = QSplitter(qOrientation.Vertical)

        # Detected creations list
        detectedGroup = QGroupBox("Detected Creations")
        detectedLayout = QVBoxLayout(detectedGroup)

        self._detectedList = QTreeWidget()
        self._detectedList.setHeaderLabels(["Name", "ID", "Files", "Status"])
        self._detectedList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._detectedList.setRootIsDecorated(False)
        detectedLayout.addWidget(self._detectedList)

        detectedBtnLayout = QHBoxLayout()
        self._scanBtn = QPushButton("Scan")
        self._scanBtn.clicked.connect(self._onScan)
        self._curateSelectedBtn = QPushButton("Curate Selected")
        self._curateSelectedBtn.clicked.connect(self._onCurateSelected)
        self._curateAllBtn = QPushButton("Curate All")
        self._curateAllBtn.clicked.connect(self._onCurateAll)
        detectedBtnLayout.addWidget(self._scanBtn)
        detectedBtnLayout.addStretch()
        detectedBtnLayout.addWidget(self._curateSelectedBtn)
        detectedBtnLayout.addWidget(self._curateAllBtn)
        detectedLayout.addLayout(detectedBtnLayout)

        splitter.addWidget(detectedGroup)

        # Curated creations list
        curatedGroup = QGroupBox("Curated Creations")
        curatedLayout = QVBoxLayout(curatedGroup)

        self._curatedList = QTreeWidget()
        self._curatedList.setHeaderLabels(["Name", "Mod Name", "Files"])
        self._curatedList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._curatedList.setRootIsDecorated(False)
        curatedLayout.addWidget(self._curatedList)

        curatedBtnLayout = QHBoxLayout()
        self._undoSelectedBtn = QPushButton("Undo Selected")
        self._undoSelectedBtn.clicked.connect(self._onUndoSelected)
        self._undoAllBtn = QPushButton("Undo All")
        self._undoAllBtn.clicked.connect(self._onUndoAll)
        curatedBtnLayout.addStretch()
        curatedBtnLayout.addWidget(self._undoSelectedBtn)
        curatedBtnLayout.addWidget(self._undoAllBtn)
        curatedLayout.addLayout(curatedBtnLayout)

        splitter.addWidget(curatedGroup)

        layout.addWidget(splitter)

        # Initial load
        self._refreshCuratedList()

        return widget

    def _createEditorTab(self) -> QWidget:
        """Creates the manual creation editor tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        descLabel = QLabel(
            "Manually add creation definitions for CC content not in the database.\n"
            "Manual entries are preserved when the database is updated."
        )
        descLabel.setWordWrap(True)
        layout.addWidget(descLabel)

        # Manual creations list
        self._manualList = QTreeWidget()
        self._manualList.setHeaderLabels(["ID", "Name", "Files"])
        self._manualList.setRootIsDecorated(False)
        self._manualList.itemSelectionChanged.connect(self._onManualSelectionChanged)
        layout.addWidget(self._manualList)

        # Editor form
        formGroup = QGroupBox("Creation Details")
        formLayout = QFormLayout(formGroup)

        self._editorId = QLineEdit()
        self._editorId.setPlaceholderText("e.g., ccBGSSSE001")
        formLayout.addRow("Creation ID:", self._editorId)

        self._editorName = QLineEdit()
        self._editorName.setPlaceholderText("e.g., Survival Mode")
        formLayout.addRow("Display Name:", self._editorName)

        self._editorFiles = QTextEdit()
        self._editorFiles.setPlaceholderText("File patterns, one per line:\nccBGSSSE001-SurvivalMode.esl\nccBGSSSE001-SurvivalMode - Main.ba2")
        self._editorFiles.setMaximumHeight(100)
        formLayout.addRow("Files:", self._editorFiles)

        self._editorDesc = QLineEdit()
        self._editorDesc.setPlaceholderText("Optional description")
        formLayout.addRow("Description:", self._editorDesc)

        layout.addWidget(formGroup)

        # Buttons
        btnLayout = QHBoxLayout()
        self._editorNewBtn = QPushButton("New")
        self._editorNewBtn.clicked.connect(self._onEditorNew)
        self._editorSaveBtn = QPushButton("Save")
        self._editorSaveBtn.clicked.connect(self._onEditorSave)
        self._editorDeleteBtn = QPushButton("Delete")
        self._editorDeleteBtn.clicked.connect(self._onEditorDelete)
        btnLayout.addWidget(self._editorNewBtn)
        btnLayout.addStretch()
        btnLayout.addWidget(self._editorSaveBtn)
        btnLayout.addWidget(self._editorDeleteBtn)
        layout.addLayout(btnLayout)

        # Load manual creations
        self._refreshManualList()

        return widget

    def _createSettingsTab(self) -> QWidget:
        """Creates the settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Group mode
        groupModeGroup = QGroupBox("Grouping Mode")
        groupModeLayout = QVBoxLayout(groupModeGroup)

        self._separateRadio = QRadioButton("Create separate mod for each creation")
        self._singleRadio = QRadioButton("Combine all creations into one mod")

        if self._settings.groupmode() == "single":
            self._singleRadio.setChecked(True)
        else:
            self._separateRadio.setChecked(True)

        self._separateRadio.toggled.connect(self._onGroupModeChanged)

        groupModeLayout.addWidget(self._separateRadio)
        groupModeLayout.addWidget(self._singleRadio)
        layout.addWidget(groupModeGroup)

        # Name format
        nameGroup = QGroupBox("Naming")
        nameLayout = QFormLayout(nameGroup)

        self._nameFormatEdit = QLineEdit(self._settings.nameformat())
        self._nameFormatEdit.textChanged.connect(self._onNameFormatChanged)
        nameLayout.addRow("Individual mod format:", self._nameFormatEdit)

        formatHelpLabel = QLabel("Use {NAME} for creation name, {ID} for creation ID")
        formatHelpLabel.setStyleSheet("color: gray; font-size: 10px;")
        nameLayout.addRow("", formatHelpLabel)

        self._combinedNameEdit = QLineEdit(self._settings.combinedname())
        self._combinedNameEdit.textChanged.connect(self._onCombinedNameChanged)
        nameLayout.addRow("Combined mod name:", self._combinedNameEdit)

        layout.addWidget(nameGroup)

        # Preview
        previewGroup = QGroupBox("Preview")
        previewLayout = QVBoxLayout(previewGroup)
        self._previewLabel = QLabel()
        self._updatePreview()
        previewLayout.addWidget(self._previewLabel)
        layout.addWidget(previewGroup)

        layout.addStretch()

        return widget

    # --- Event Handlers ---

    def _onScan(self):
        """Handles scan button click."""
        self._detectedList.clear()
        self._scanResults = []

        matched, unmatched = self._curationclub.scanForCreations()

        for creation, files in matched:
            if not self._curationclub.isCreationCurated(creation[CREATION_ID]):
                item = QTreeWidgetItem([
                    creation[CREATION_NAME],
                    creation[CREATION_ID],
                    str(len(files)),
                    "Detected"
                ])
                item.setData(0, qItemDataRole.UserRole, (creation, files))
                self._detectedList.addTopLevelItem(item)
                self._scanResults.append((creation, files))

        if unmatched:
            self._log.info(f"Found {len(unmatched)} unmatched CC files")
            # Show message about unmatched files
            QMessageBox.information(
                self._dialog,
                "Scan Complete",
                f"Found {len(self._scanResults)} known creations.\n"
                f"{len(unmatched)} files could not be matched to known creations.\n"
                "Use the Manual Editor tab to add definitions for unknown creations."
            )
        else:
            QMessageBox.information(
                self._dialog,
                "Scan Complete",
                f"Found {len(self._scanResults)} creations ready to curate."
            )

    def _onCurateSelected(self):
        """Curates selected creations."""
        selected = self._detectedList.selectedItems()
        if not selected:
            return

        count = 0
        for item in selected:
            data = item.data(0, qItemDataRole.UserRole)
            if data:
                creation, files = data
                if self._curationclub.curateCreation(creation, files):
                    count += 1

        QMessageBox.information(
            self._dialog,
            "Curation Complete",
            f"Successfully curated {count} creation(s).\n"
            "Refresh MO2 to see the new mods."
        )

        self._onScan()  # Refresh detected list
        self._refreshCuratedList()
        self._organiser.refresh()

    def _onCurateAll(self):
        """Curates all detected creations."""
        if not self._scanResults:
            return

        count = self._curationclub.curateAll(self._scanResults)

        QMessageBox.information(
            self._dialog,
            "Curation Complete",
            f"Successfully curated {count} creation(s).\n"
            "Refresh MO2 to see the new mods."
        )

        self._onScan()
        self._refreshCuratedList()
        self._organiser.refresh()

    def _onUndoSelected(self):
        """Undoes selected curations."""
        selected = self._curatedList.selectedItems()
        if not selected:
            return

        count = 0
        for item in selected:
            creationId = item.data(0, qItemDataRole.UserRole)
            if creationId and self._curationclub.undoCuration(creationId):
                count += 1

        QMessageBox.information(
            self._dialog,
            "Undo Complete",
            f"Successfully restored {count} creation(s) to game folder."
        )

        self._refreshCuratedList()
        self._organiser.refresh()

    def _onUndoAll(self):
        """Undoes all curations."""
        curated = self._curationclub.getCuratedCreations()
        if not curated:
            return

        reply = QMessageBox.question(
            self._dialog,
            "Confirm Undo All",
            f"This will restore {len(curated)} creation(s) to the game folder.\nContinue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            count = self._curationclub.undoAll()
            QMessageBox.information(
                self._dialog,
                "Undo Complete",
                f"Successfully restored {count} creation(s) to game folder."
            )
            self._refreshCuratedList()
            self._organiser.refresh()

    def _refreshCuratedList(self):
        """Refreshes the curated creations list."""
        self._curatedList.clear()
        curated = self._curationclub.getCuratedCreations()

        for creationId, curation in curated.items():
            item = QTreeWidgetItem([
                curation["name"],
                curation["modName"],
                str(len(curation["destFiles"]))
            ])
            item.setData(0, qItemDataRole.UserRole, creationId)
            self._curatedList.addTopLevelItem(item)

    def _refreshManualList(self):
        """Refreshes the manual creations list."""
        self._manualList.clear()
        database = self._curationclub.loadCreationsDatabase()

        for creationId, creation in database.items():
            if creation.get(CREATION_MANUAL, False):
                files = creation.get(CREATION_FILES, [])
                item = QTreeWidgetItem([
                    creation[CREATION_ID],
                    creation[CREATION_NAME],
                    str(len(files))
                ])
                item.setData(0, qItemDataRole.UserRole, creation)
                self._manualList.addTopLevelItem(item)

    def _onManualSelectionChanged(self):
        """Handles manual list selection change."""
        selected = self._manualList.selectedItems()
        if selected:
            creation = selected[0].data(0, qItemDataRole.UserRole)
            self._editorId.setText(creation.get(CREATION_ID, ""))
            self._editorName.setText(creation.get(CREATION_NAME, ""))
            self._editorFiles.setPlainText("\n".join(creation.get(CREATION_FILES, [])))
            self._editorDesc.setText(creation.get(CREATION_DESCRIPTION, ""))

    def _onEditorNew(self):
        """Clears the editor for a new entry."""
        self._manualList.clearSelection()
        self._editorId.clear()
        self._editorName.clear()
        self._editorFiles.clear()
        self._editorDesc.clear()
        self._editorId.setFocus()

    def _onEditorSave(self):
        """Saves the current editor content."""
        creationId = self._editorId.text().strip().lower()
        name = self._editorName.text().strip()
        files = [f.strip() for f in self._editorFiles.toPlainText().split("\n") if f.strip()]
        desc = self._editorDesc.text().strip()

        if not creationId or not name:
            QMessageBox.warning(
                self._dialog,
                "Validation Error",
                "Creation ID and Name are required."
            )
            return

        creation = createCreationData(creationId, name, files, desc, manual=True)

        if self._curationclub.saveManualCreation(creation):
            QMessageBox.information(
                self._dialog,
                "Saved",
                f"Creation '{name}' saved successfully."
            )
            self._refreshManualList()
            self._onEditorNew()
        else:
            QMessageBox.warning(
                self._dialog,
                "Error",
                "Failed to save creation."
            )

    def _onEditorDelete(self):
        """Deletes the selected manual creation."""
        creationId = self._editorId.text().strip().lower()
        if not creationId:
            return

        reply = QMessageBox.question(
            self._dialog,
            "Confirm Delete",
            f"Delete manual creation '{creationId}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self._curationclub.deleteManualCreation(creationId):
                self._refreshManualList()
                self._onEditorNew()

    def _onGroupModeChanged(self, checked: bool):
        """Handles group mode radio button change."""
        if self._separateRadio.isChecked():
            self._settings.updateGroupmode("separate")
        else:
            self._settings.updateGroupmode("single")
        self._updatePreview()

    def _onNameFormatChanged(self, text: str):
        """Handles name format change."""
        self._settings.updateNameformat(text)
        self._updatePreview()

    def _onCombinedNameChanged(self, text: str):
        """Handles combined name change."""
        self._settings.updateCombinedname(text)
        self._updatePreview()

    def _updatePreview(self):
        """Updates the preview label."""
        if self._settings.groupmode() == "single":
            preview = f"All creations will be placed in: {self._settings.combinedname()}"
        else:
            example = self._settings.nameformat()
            example = example.replace("{NAME}", "Survival Mode")
            example = example.replace("{ID}", "ccBGSSSE001")
            preview = f"Example mod name: {example}"
        self._previewLabel.setText(preview)
