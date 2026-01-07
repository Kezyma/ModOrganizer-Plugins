import mobase, webbrowser
from pathlib import Path
try:
    from ..ui.qt6.openmwplayer_menu import Ui_OMWPMenu
    from ..ui.qt6.openmwplayer_options import Ui_omwp_optionswidget
    from ..ui.qt6.openmwplayer_groundcover import Ui_omwp_groundcoverwidget
    from ..ui.qt6.openmwplayer_settings import Ui_omwp_settingswidget
    from ..ui.qt6.openmwplayer_settingsrow import Ui_omwp_settingsrow
    from ..ui.qt6.openmwplayer_settingsrowcheck import Ui_omwp_settingsrow_check
    from ..ui.qt6.openmwplayer_settingsrow_comment import Ui_omwp_settingsrow_comment
    from ..ui.qt6.openmwplayer_settingsrowcheck_comment import Ui_omwp_settingsrow_check_comment
    from ..ui.qt6.openmwplayer_archives import Ui_omwp_archiveswidget
    from ..ui.qt6.openmwplayer_openmwcfg import Ui_omwp_cfgwidget
    from ....base.ui.qt6.update_widget import Ui_updateTabWidget
except:
    from ..ui.qt5.openmwplayer_menu import Ui_OMWPMenu
    from ..ui.qt5.openmwplayer_options import Ui_omwp_optionswidget
    from ..ui.qt5.openmwplayer_groundcover import Ui_omwp_groundcoverwidget
    from ..ui.qt5.openmwplayer_settings import Ui_omwp_settingswidget
    from ..ui.qt5.openmwplayer_settingsrow import Ui_omwp_settingsrow
    from ..ui.qt5.openmwplayer_settingsrowcheck import Ui_omwp_settingsrow_check
    from ..ui.qt5.openmwplayer_settingsrow_comment import Ui_omwp_settingsrow_comment
    from ..ui.qt5.openmwplayer_settingsrowcheck_comment import Ui_omwp_settingsrow_check_comment
    from ..ui.qt5.openmwplayer_archives import Ui_omwp_archiveswidget
    from ..ui.qt5.openmwplayer_openmwcfg import Ui_omwp_cfgwidget
    from ....base.ui.qt5.update_widget import Ui_updateTabWidget

from ..core.openmwplayer import OpenMWPlayer
from .openmwplayer_texteditor import OpenMWPlayerTextEditor
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ....common.common_icons import *
from ....common.common_qt import *
from ....common.common_utilities import loadLines, saveLines

class OpenMWPlayerMenu(QtWidgets.QWidget):
    """OpenMW main widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, openmwPlayer:OpenMWPlayer, update:CommonUpdate, help:CommonHelp):
        super().__init__(parent)
        self._organiser = organiser
        self._openmwPlayer = openmwPlayer
        self._update = update
        self._help = help
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_OMWPMenu()
        self.widget.setupUi(self)

        self.optionsWidget = Ui_omwp_optionswidget()
        self.optionsWidget.setupUi(self.widget.optionsTab)

        self.groundcoverWidget = Ui_omwp_groundcoverwidget()
        self.groundcoverWidget.setupUi(self.widget.groundcoverTab)

        self.openmwcfgWidget = Ui_omwp_cfgwidget()
        self.openmwcfgWidget.setupUi(self.widget.openmwcfgTab)

        self.archivesWidget = Ui_omwp_archiveswidget()
        self.archivesWidget.setupUi(self.widget.archivesTab)

        self.settingsWidget = Ui_omwp_settingswidget()
        self.settingsWidget.setupUi(self.widget.settingscfgTab)

        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)

        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self._update.configure(self.updateTabWidget)
        self._help.configure(self.helpTabWidget)

        self.optionsWidget.btnImport.setIcon(SYNC_ICON)
        self.optionsWidget.btnExport.setIcon(LINK_ICON)

        # Connect text editor buttons
        self.settingsWidget.btnEditText.clicked.connect(self._editSettingsCfgRaw)
        self.openmwcfgWidget.btnEditText.clicked.connect(self._editOpenmwCfgRaw)

    _settingsCfg = {}
    _openmwCfg = {}
    _groundcoverData = []  # List of {"name": str, "enabled": bool, "loadOrder": int}

    def rebind(self):
        self._settingsCfg = self._openmwPlayer._files.getCompleteSettingsCfg()
        self._openmwCfg = self._openmwPlayer._files.getCustomOpenmwCfg()
        self.rebindOptions()
        self.rebindSettingsCfg()
        self.rebindOpenmwCfg()

    def rebindOptions(self):
        cfgPath = self._openmwPlayer._strings.openmwCfgPath()
        self.optionsWidget.lblConfig.setText(cfgPath)
        self.optionsWidget.btnConfig.clicked.connect(self.selectOpenmwCfgPath)

        dummyEsp = self._openmwPlayer._settings.dummyesp()
        self.optionsWidget.chkDummy.setChecked(dummyEsp)
        self.optionsWidget.chkDummy.stateChanged.connect(self.toggleDummyEsp)

        self.optionsWidget.btnImport.clicked.connect(self.importOpenmwCfg)
        self.optionsWidget.btnExport.clicked.connect(self.exportOpenmwCfg)

    def selectOpenmwCfgPath(self):
        manualPath = Path(QFileDialog.getOpenFileName(None, "Locate OpenMW Config File", ".", "OpenMW Config File (openmw.cfg)")[0])
        if len(str(manualPath)) > 0 and manualPath.exists():
            self._openmwPlayer._settings.updateSetting("openmwcfgpath", str(manualPath))
            self.optionsWidget.lblConfig.setText(str(manualPath))

    def toggleDummyEsp(self):
        enabled = self.optionsWidget.chkDummy.isChecked()
        self._openmwPlayer.toggleDummyEsps(enabled)

    def importOpenmwCfg(self):
        self._openmwPlayer.importSettings()
        self._openmwCfg = self._openmwPlayer._files.getCustomOpenmwCfg()
        self._settingsCfg = self._openmwPlayer._files.getCompleteSettingsCfg()
        self.rebindOpenmwCfg()
        self.rebindSettingsCfg()

    def exportOpenmwCfg(self):
        self._openmwPlayer._import.exportOpenmwCfg()
        self._openmwPlayer._import.exportSettingsCfg()

    def rebindOpenmwCfg(self):
        self.rebindCustomOpenmwCfg()
        self.rebindArchivesOpenmwCfg()
        self.rebindGroundcoverOpenmwCfg()

    def rebindArchivesOpenmwCfg(self):
        try:
            self.archivesWidget.lstArchives.indexesMoved.disconnect()
            self.archivesWidget.lstArchives.itemChanged.disconnect()
            self.archivesWidget.lstArchives.currentRowChanged.disconnect()
            self.archivesWidget.lstArchives.currentItemChanged.disconnect()
            self.archivesWidget.lstArchives.model().rowsMoved.disconnect()
        except:
            pass
        self.archivesWidget.lstArchives.clear()
        archiveOptions = self._openmwPlayer._files.getArchiveOptions()
        for archive in self._openmwCfg["Archives"]:
            item = QtWidgets.QListWidgetItem()
            item.setText(archive)
            item.setFlags(item.flags() | qItemFlag.ItemIsUserCheckable | qItemFlag.ItemIsEnabled)
            item.setCheckState(qCheckState.Checked)
            self.archivesWidget.lstArchives.addItem(item)
        for archive in archiveOptions:
            if archive not in self._openmwCfg["Archives"]:
                item = QtWidgets.QListWidgetItem()
                item.setText(archive)
                item.setFlags(item.flags() | qItemFlag.ItemIsUserCheckable | qItemFlag.ItemIsEnabled)
                item.setCheckState(qCheckState.Unchecked)
                self.archivesWidget.lstArchives.addItem(item)
        self.archivesWidget.lstArchives.indexesMoved.connect(self.saveArchivesOpenmwCfg)
        self.archivesWidget.lstArchives.itemChanged.connect(self.saveArchivesOpenmwCfg)
        self.archivesWidget.lstArchives.currentRowChanged.connect(self.saveArchivesOpenmwCfg)
        self.archivesWidget.lstArchives.currentItemChanged.connect(self.saveArchivesOpenmwCfg)
        self.archivesWidget.lstArchives.model().rowsMoved.connect(self.saveArchivesOpenmwCfg)

    def saveArchivesOpenmwCfg(self):
        selected = []
        for ix in range(self.archivesWidget.lstArchives.count()):
            row = self.archivesWidget.lstArchives.item(ix)
            if row.checkState() == qCheckState.Checked:
                selected.append(row.text())
        self._openmwCfg["Archives"] = selected
        self.saveOpenmwCfg()

    def rebindGroundcoverOpenmwCfg(self):
        # Disconnect existing signals
        try:
            self.groundcoverWidget.lstGroundcover.indexesMoved.disconnect()
            self.groundcoverWidget.lstGroundcover.itemChanged.disconnect()
            self.groundcoverWidget.lstGroundcover.currentRowChanged.disconnect()
            self.groundcoverWidget.lstGroundcover.currentItemChanged.disconnect()
            self.groundcoverWidget.txtFilter.textChanged.disconnect()
            self.groundcoverWidget.cmbSort.currentIndexChanged.disconnect()
        except:
            pass

        # Build data list with position from profile's loadorder.txt
        groundcoverOptions = self._openmwPlayer._files.getGroundcoverOptions()

        # Read load order from profile's loadorder.txt (contains all plugins in order)
        profilePath = self._organiser.profile().absolutePath()
        loadOrderPath = Path(profilePath) / "loadorder.txt"
        pluginPositions = {}
        if loadOrderPath.exists():
            loadOrderLines = loadLines(str(loadOrderPath))
            if loadOrderLines:
                pluginPositions = {line.strip().lower(): idx for idx, line in enumerate(loadOrderLines) if line.strip()}

        self._groundcoverData = []
        for esp in groundcoverOptions:
            # Transform name for OpenMW compatibility
            espName = str(esp).replace(".omwaddon.esp", ".omwaddon").replace(".omwscripts.esp", ".omwscripts")
            # Get position from loadorder.txt (works for both active and inactive plugins)
            pluginPosition = pluginPositions.get(esp.lower(), 999999)
            self._groundcoverData.append({
                "name": espName,
                "enabled": espName in self._openmwCfg["Groundcover"],
                "loadOrder": pluginPosition
            })

        # Connect filter/sort controls
        self.groundcoverWidget.txtFilter.textChanged.connect(self._updateGroundcoverList)
        self.groundcoverWidget.cmbSort.currentIndexChanged.connect(self._updateGroundcoverList)

        # Initial display
        self._updateGroundcoverList()

        # Connect save signals
        self.groundcoverWidget.lstGroundcover.itemChanged.connect(self.saveGroundcoverOpenmwCfg)

    def _updateGroundcoverList(self):
        """Update list widget based on current filter and sort settings."""
        try:
            self.groundcoverWidget.lstGroundcover.itemChanged.disconnect()
        except:
            pass

        self.groundcoverWidget.lstGroundcover.clear()
        filterText = self.groundcoverWidget.txtFilter.text().lower()
        sortIndex = self.groundcoverWidget.cmbSort.currentIndex()

        # Sort data
        sortedData = self._groundcoverData.copy()
        if sortIndex == 0:  # Load Order
            sortedData.sort(key=lambda x: x["loadOrder"])
        elif sortIndex == 1:  # A-Z
            sortedData.sort(key=lambda x: x["name"].lower())
        elif sortIndex == 2:  # Z-A
            sortedData.sort(key=lambda x: x["name"].lower(), reverse=True)

        # Filter and display
        for item in sortedData:
            if filterText and filterText not in item["name"].lower():
                continue
            listItem = QtWidgets.QListWidgetItem()
            listItem.setText(item["name"])
            listItem.setFlags(listItem.flags() | qItemFlag.ItemIsUserCheckable | qItemFlag.ItemIsEnabled)
            listItem.setCheckState(qCheckState.Checked if item["enabled"] else qCheckState.Unchecked)
            self.groundcoverWidget.lstGroundcover.addItem(listItem)

        self.groundcoverWidget.lstGroundcover.itemChanged.connect(self.saveGroundcoverOpenmwCfg)

    def saveGroundcoverOpenmwCfg(self):
        """Save groundcover selection, updating internal data."""
        selected = []
        for ix in range(self.groundcoverWidget.lstGroundcover.count()):
            row = self.groundcoverWidget.lstGroundcover.item(ix)
            itemName = row.text()
            isChecked = row.checkState() == qCheckState.Checked

            # Update internal data structure
            for item in self._groundcoverData:
                if item["name"] == itemName:
                    item["enabled"] = isChecked
                    break

            if isChecked:
                selected.append(itemName)

        self._openmwCfg["Groundcover"] = selected
        self.saveOpenmwCfg()

    def rebindCustomOpenmwCfg(self):
        self.openmwcfgWidget.configTabs.clear()
        customCfg = self._openmwCfg["Settings"]
        # Get all the categories to use as tabs
        tabNames = []
        for setting in customCfg:
            category = str(setting).split("_")[0]
            if category not in tabNames:
                tabNames.append(category)
        
        scrollLayoutCollection = {}
        scrollAreaCollection = {}
        for tabName in tabNames:
            # Create the base tab widget for this tab.
            newSettingTab = QWidget()
            newSettingLayout = QtWidgets.QVBoxLayout(newSettingTab)
            newSettingLayout.setContentsMargins(0, 0, 0, 0)
            self.openmwcfgWidget.configTabs.addTab(newSettingTab, QIcon(), tabName)

            # Add the scroll area to the tab
            scrollArea = QtWidgets.QScrollArea(parent=newSettingTab)
            scrollArea.setWidgetResizable(True)
            scrollAreaWidget = QWidget()
            scrollAreaLayout = QtWidgets.QVBoxLayout(scrollAreaWidget)
            scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
            scrollAreaLayout.setSpacing(0)
            scrollArea.setWidget(scrollAreaWidget)
            newSettingLayout.addWidget(scrollArea)
            scrollAreaCollection[tabName] = scrollAreaWidget
            scrollLayoutCollection[tabName] = scrollAreaLayout

        for setting in customCfg:
            category = str(setting).split("_")[0]
            tabWidget = scrollAreaCollection[category]
            tabLayout = scrollLayoutCollection[category]
            newSettingWidget = QWidget(parent=tabWidget)
            newSettingRow = Ui_omwp_settingsrow()
            newSettingRow.setupUi(newSettingWidget)
            newSettingRow.txtSetting.setText(customCfg[setting])
            newSettingRow.lblSetting.setText(setting)
            newSettingRow.txtSetting.editingFinished.connect(lambda s=setting, x=newSettingRow.txtSetting: self.updateTextCustomOpenmwCfg(s, x.text()))
            tabLayout.addWidget(newSettingWidget)

        for tab in scrollLayoutCollection:
            spacerItem = QtWidgets.QSpacerItem(40, 0, qSizePolicy.Minimum, qSizePolicy.Expanding)
            scrollLayoutCollection[tab].addItem(spacerItem)

    def updateTextCustomOpenmwCfg(self, setting:str, value:str):
        self._openmwCfg["Settings"][setting] = value
        self.saveOpenmwCfg()

    def saveOpenmwCfg(self):
        dataFiles = self._openmwPlayer._files.getDataFolders()
        loadOrder = self._openmwPlayer._files.getEnabledPlugins()
        self._openmwCfg["Data"] = dataFiles
        self._openmwCfg["Content"] = loadOrder
        cfgPath = self._openmwPlayer._strings.customOpenmwCfgPath()
        self._openmwPlayer._files.saveOpenmwCfg(cfgPath, self._openmwCfg)

    def _getSettingValue(self, category: str, setting: str) -> str:
        """Get setting value, handling both string and dict formats."""
        data = self._settingsCfg[category][setting]
        if isinstance(data, dict):
            return data.get("value", "")
        return data

    def _getSettingComment(self, category: str, setting: str) -> str:
        """Get setting comment, or empty string if none."""
        data = self._settingsCfg[category][setting]
        if isinstance(data, dict):
            return data.get("comment", "")
        return ""

    def _setSettingValue(self, category: str, setting: str, value: str):
        """Set setting value, preserving comment if present."""
        data = self._settingsCfg[category][setting]
        if isinstance(data, dict):
            data["value"] = value
        else:
            self._settingsCfg[category][setting] = {"value": value, "comment": ""}

    def updateTextSettingsCfg(self, category:str, setting:str, value:str):
        self._openmwPlayer._log.info(f"Updating [{category}] {setting} = {value}")
        self._setSettingValue(category, setting, value)
        self.saveSettingsCfg()

    def updateBoolSettingsCfg(self, category:str, setting:str, value:bool):
        self._openmwPlayer._log.info(f"Updating [{category}] {setting} = {str(value).lower()}")
        self._setSettingValue(category, setting, "true" if value else "false")
        self.saveSettingsCfg()

    def saveSettingsCfg(self):
        cfgPath = self._openmwPlayer._strings.customSettingsCfgPath()
        self._openmwPlayer._files.saveSettingsCfg(cfgPath, self._settingsCfg)
        # Don't rebuild UI - the data dict is already updated and widgets show correct values
        # This matches how saveOpenmwCfg() works and preserves scroll position

    def rebindSettingsCfg(self):
        self.settingsWidget.settingsTabs.clear()
        for category in self._settingsCfg:

            # Create the base tab widget for this tab.
            newSettingTab = QWidget()
            newSettingLayout = QtWidgets.QVBoxLayout(newSettingTab)
            newSettingLayout.setContentsMargins(0, 0, 0, 0)
            self.settingsWidget.settingsTabs.addTab(newSettingTab, QIcon(), category)

            # Add the scroll area to the tab
            scrollArea = QtWidgets.QScrollArea(parent=newSettingTab)
            scrollArea.setWidgetResizable(True)
            scrollAreaWidget = QWidget()
            scrollAreaLayout = QtWidgets.QVBoxLayout(scrollAreaWidget)
            scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
            scrollAreaLayout.setSpacing(0)
            scrollArea.setWidget(scrollAreaWidget)
            newSettingLayout.addWidget(scrollArea)

            for setting in self._settingsCfg[category]:
                settingValue = self._getSettingValue(category, setting)
                settingComment = self._getSettingComment(category, setting)
                self._openmwPlayer._log.debug(f"Binding [{category}] {setting} = {settingValue}")

                newSettingWidget = QWidget(parent=scrollAreaWidget)

                if settingValue == "true" or settingValue == "false":
                    # Boolean: use checkbox (with or without comment)
                    if settingComment:
                        newSettingRow = Ui_omwp_settingsrow_check_comment()
                        newSettingRow.setupUi(newSettingWidget)
                        newSettingRow.chkSetting.setChecked(settingValue == "true")
                        newSettingRow.lblSetting.setText(setting)
                        newSettingRow.lblComment.setText(settingComment)
                        newSettingRow.chkSetting.stateChanged.connect(lambda _, c=category, s=setting, x=newSettingRow.chkSetting: self.updateBoolSettingsCfg(c, s, x.isChecked()))
                    else:
                        newSettingRow = Ui_omwp_settingsrow_check()
                        newSettingRow.setupUi(newSettingWidget)
                        newSettingRow.chkSetting.setChecked(settingValue == "true")
                        newSettingRow.lblSetting.setText(setting)
                        newSettingRow.chkSetting.stateChanged.connect(lambda _, c=category, s=setting, x=newSettingRow.chkSetting: self.updateBoolSettingsCfg(c, s, x.isChecked()))
                elif settingComment:
                    # Text with comment
                    newSettingRow = Ui_omwp_settingsrow_comment()
                    newSettingRow.setupUi(newSettingWidget)
                    newSettingRow.txtSetting.setText(settingValue)
                    newSettingRow.lblSetting.setText(setting)
                    newSettingRow.lblComment.setText(settingComment)
                    newSettingRow.txtSetting.editingFinished.connect(lambda c=category, s=setting, x=newSettingRow.txtSetting: self.updateTextSettingsCfg(c, s, x.text()))
                else:
                    # Text without comment
                    newSettingRow = Ui_omwp_settingsrow()
                    newSettingRow.setupUi(newSettingWidget)
                    newSettingRow.txtSetting.setText(settingValue)
                    newSettingRow.lblSetting.setText(setting)
                    newSettingRow.txtSetting.editingFinished.connect(lambda c=category, s=setting, x=newSettingRow.txtSetting: self.updateTextSettingsCfg(c, s, x.text()))

                scrollAreaLayout.addWidget(newSettingWidget)

            spacerItem = QtWidgets.QSpacerItem(40, 0, qSizePolicy.Minimum, qSizePolicy.Expanding)
            scrollAreaLayout.addItem(spacerItem)

    def _editSettingsCfgRaw(self):
        """Open text editor for settings.cfg."""
        cfgPath = self._openmwPlayer._strings.customSettingsCfgPath()
        if Path(cfgPath).exists():
            lines = loadLines(cfgPath)
            content = "\n".join(lines) if lines else ""
        else:
            content = ""

        result = OpenMWPlayerTextEditor.edit(self, "Edit settings.cfg", content)

        if result is not None:
            # Save with proper line endings
            lines = [line + "\n" for line in result.rstrip("\n").split("\n")]
            if saveLines(cfgPath, lines):
                self._openmwPlayer._log.debug("Saved raw settings.cfg")
                self._settingsCfg = self._openmwPlayer._files.getCompleteSettingsCfg()
                self.rebindSettingsCfg()

    def _editOpenmwCfgRaw(self):
        """Open text editor for openmw.cfg."""
        cfgPath = self._openmwPlayer._strings.customOpenmwCfgPath()
        if Path(cfgPath).exists():
            lines = loadLines(cfgPath)
            content = "\n".join(lines) if lines else ""
        else:
            content = ""

        result = OpenMWPlayerTextEditor.edit(self, "Edit openmw.cfg", content)

        if result is not None:
            lines = [line + "\n" for line in result.rstrip("\n").split("\n")]
            if saveLines(cfgPath, lines):
                self._openmwPlayer._log.debug("Saved raw openmw.cfg")
                self._openmwCfg = self._openmwPlayer._files.getCustomOpenmwCfg()
                self.rebindOpenmwCfg()
