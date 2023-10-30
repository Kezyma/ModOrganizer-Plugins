import mobase, webbrowser
from pathlib import Path
try:
    from ..ui.qt6.rootbuilder_menu import Ui_RootBuilderMenu
    from ..ui.qt6.rootbuilder_mode import Ui_modeTabWidget
    from ..ui.qt6.rootbuilder_custom import Ui_customTabWidget
    from ..ui.qt6.rootbuilder_settings import Ui_settingsTabWidget
    from ..ui.qt6.rootbuilder_exclusions import Ui_exclusionsTabWidget
    from ..ui.qt6.rootbuilder_actions import Ui_actionsTabWidget
    from ..ui.qt6.rootbuilder_help import Ui_helpTabWidget
    from ..ui.qt6.rootbuilder_update import Ui_updateTabWidget
    from ..ui.qt6.rootbuilder_export import Ui_exportTabWidget
except:
    from ..ui.qt5.rootbuilder_menu import Ui_RootBuilderMenu
    from ..ui.qt5.rootbuilder_mode import Ui_modeTabWidget
    from ..ui.qt5.rootbuilder_custom import Ui_customTabWidget
    from ..ui.qt5.rootbuilder_settings import Ui_settingsTabWidget
    from ..ui.qt5.rootbuilder_exclusions import Ui_exclusionsTabWidget
    from ..ui.qt5.rootbuilder_actions import Ui_actionsTabWidget
    from ..ui.qt5.rootbuilder_help import Ui_helpTabWidget
    from ..ui.qt5.rootbuilder_update import Ui_updateTabWidget
    from ..ui.qt5.rootbuilder_export import Ui_exportTabWidget

from ..core.rootbuilder import RootBuilder
from .rootbuilder_update import RootBuilderUpdate
from ....common.common_icons import CommonIcons
from ....common.common_qt import *

class RootBuilderMenu(QtWidgets.QWidget):
    """Root Builder menu widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, rootBuilder:RootBuilder, update:RootBuilderUpdate):
        super().__init__(parent)
        self._organiser = organiser
        self._rootBuilder = rootBuilder
        self._update = update
        self._rebind = False
        self._icons = CommonIcons()
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_RootBuilderMenu()
        self.widget.setupUi(self)

        self.modeTabWidget = Ui_modeTabWidget()
        self.modeTabWidget.setupUi(self.widget.modeTab)
        self.customTabWidget = Ui_customTabWidget()
        self.customTabWidget.setupUi(self.widget.customModeTab)
        self.settingsTabWidget = Ui_settingsTabWidget()
        self.settingsTabWidget.setupUi(self.widget.settingsTab)
        self.exclusionsTabWidget = Ui_exclusionsTabWidget()
        self.exclusionsTabWidget.setupUi(self.widget.exclusionsTab)
        self.actionsTabWidget = Ui_actionsTabWidget()
        self.actionsTabWidget.setupUi(self.widget.actionsTab)
        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)
        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)
        self.exportTabWidget = Ui_exportTabWidget()
        self.exportTabWidget.setupUi(self.widget.exportTab)

        self.updateTabWidget.updateFoundWidget.setVisible(False)
        self.updateTabWidget.noUpdateWidget.setVisible(False)
        self.updateTabWidget.checkUpdateButton.setIcon(self._icons.refreshIcon())
        self.updateTabWidget.updateFoundButton.setIcon(self._icons.downloadIcon())
        self.updateTabWidget.updateFoundButton.clicked.connect(self.updateFound_clicked)
        self.updateTabWidget.checkUpdateButton.clicked.connect(self.checkUpdate_clicked)

        self.modeTabWidget.copyModeRadio.clicked.connect(self.copyModeButton_clicked)
        self.modeTabWidget.usvfsModeRadio.clicked.connect(self.usvfsModeButton_clicked)
        self.modeTabWidget.linkModeRadio.clicked.connect(self.linkModeButton_clicked)
        self.modeTabWidget.usvfsLinkModeRadio.clicked.connect(self.usvfslinkModeButton_clicked)
        self.modeTabWidget.customModeRadio.clicked.connect(self.customModeButton_clicked)

        self.customTabWidget.copyModePrioritySpin.valueChanged.connect(self.copyModePrioritySpin_changed)
        self.customTabWidget.linkModePrioritySpin.valueChanged.connect(self.linkModePrioritySpin_changed)
        self.customTabWidget.usvfsModePrioritySpin.valueChanged.connect(self.usvfsModePrioritySpin_changed)
        
        self.customTabWidget.copyModeTable.cellChanged.connect(self.copyModeTable_cellChanged)
        self.customTabWidget.linkModeTable.cellChanged.connect(self.linkModeTable_cellChanged)
        self.customTabWidget.usvfsModeTable.cellChanged.connect(self.usvfsModeTable_cellChanged)

        self.settingsTabWidget.backupCheck.stateChanged.connect(self.backupCheck_changed)
        self.settingsTabWidget.cacheCheck.stateChanged.connect(self.cacheCheck_changed)
        self.settingsTabWidget.autobuildCheck.stateChanged.connect(self.autobuildCheck_changed)
        self.settingsTabWidget.redirectCheck.stateChanged.connect(self.redirectCheck_changed)
        self.settingsTabWidget.installerCheck.stateChanged.connect(self.installerCheck_changed)
        self.settingsTabWidget.debugLevelCombo.currentTextChanged.connect(self.debugModeCombo_changed)
        self.settingsTabWidget.hashCheck.stateChanged.connect(self.hashCheck_changed)

        self.exclusionsTabWidget.exclusionsTable.cellChanged.connect(self.exclusionsTable_cellChanged)

        self.actionsTabWidget.buildButton.setIcon(self._icons.plusIcon())
        self.actionsTabWidget.buildButton.clicked.connect(self.build_clicked)
        self.actionsTabWidget.syncButton.setIcon(self._icons.syncIcon())
        self.actionsTabWidget.syncButton.clicked.connect(self.sync_clicked)
        self.actionsTabWidget.clearButton.setIcon(self._icons.minusIcon())
        self.actionsTabWidget.clearButton.clicked.connect(self.clear_clicked)
        self.actionsTabWidget.cacheDeleteButton.setIcon(self._icons.trashIcon())
        self.actionsTabWidget.cacheDeleteButton.clicked.connect(self.deleteCache_clicked)
        self.actionsTabWidget.cacheCreateButton.setIcon(self._icons.refreshIcon())
        self.actionsTabWidget.cacheCreateButton.clicked.connect(self.createCache_clicked)
        self.actionsTabWidget.backupDeleteButton.setIcon(self._icons.trashIcon())
        self.actionsTabWidget.backupDeleteButton.clicked.connect(self.deleteBackup_clicked)
        self.actionsTabWidget.backupCreateButton.setIcon(self._icons.refreshIcon())
        self.actionsTabWidget.backupCreateButton.clicked.connect(self.createBackup_clicked)

        self.helpTabWidget.discordButton.setIcon(self._icons.discordIcon())
        self.helpTabWidget.discordButton.clicked.connect(self.discord_clicked)
        self.helpTabWidget.docsButton.setIcon(self._icons.docsIcon())
        self.helpTabWidget.docsButton.clicked.connect(self.docs_clicked)
        self.helpTabWidget.githubButton.setIcon(self._icons.githubIcon())
        self.helpTabWidget.githubButton.clicked.connect(self.github_clicked)
        self.helpTabWidget.nexusButton.setIcon(self._icons.nexusIcon())
        self.helpTabWidget.nexusButton.clicked.connect(self.nexus_clicked)
        self.helpTabWidget.patreonButton.setIcon(self._icons.patreonIcon())
        self.helpTabWidget.patreonButton.clicked.connect(self.patreon_clicked)

        helpPath = Path(__file__).parent.parent / "docs" / "readme.html"
        helpUrl = QtCore.QUrl.fromLocalFile(str(helpPath.absolute()))
        self.helpTabWidget.helpText.setSource(helpUrl)

        self.exportTabWidget.exportButton.clicked.connect(self.exportButton_clicked)
        self.exportTabWidget.exportButton.setIcon(self._icons.linkIcon())
        self.exportTabWidget.importButton.clicked.connect(self.importButton_clicked)
        self.exportTabWidget.importButton.setIcon(self._icons.downloadIcon())
        self.exportTabWidget.resetButton.clicked.connect(self.resetButton_clicked)
        self.exportTabWidget.resetButton.setIcon(self._icons.refreshIcon())
    

    def rebind(self):
        """Rebinds the settings and visibility."""
        self._rebind = True
        self.bindModeTabs()
        self.bindModeWhitelistTables()
        self.bindSettingsTab()
        self.bindExclusionsTable()
        self.bindActionButtons()
        self._rebind = False

    def bindSettingsTab(self):
        """Binds the settings tab."""
        cacheEnabled = self._rootBuilder._settings.cache()
        backupEnabled = self._rootBuilder._settings.backup()
        autobuildEnabled = self._rootBuilder._settings.autobuild()
        redirectEnabled = self._rootBuilder._settings.redirect()
        installerEnabled = self._rootBuilder._settings.installer()
        loglevel = self._rootBuilder._settings.loglevel()
        hashEnabled = self._rootBuilder._settings.hash()
        noBuild = not self._rootBuilder._data.dataFileExists()

        self.settingsTabWidget.cacheCheck.setEnabled(noBuild)
        self.settingsTabWidget.backupCheck.setEnabled(noBuild)
        self.settingsTabWidget.autobuildCheck.setEnabled(noBuild)
        self.settingsTabWidget.redirectCheck.setEnabled(noBuild)
        self.settingsTabWidget.installerCheck.setEnabled(noBuild)
        self.settingsTabWidget.debugLevelCombo.setEnabled(noBuild)
        self.settingsTabWidget.hashCheck.setEnabled(noBuild)

        self.settingsTabWidget.cacheCheck.setChecked(cacheEnabled)
        self.settingsTabWidget.backupCheck.setChecked(backupEnabled)
        self.settingsTabWidget.autobuildCheck.setChecked(autobuildEnabled)
        self.settingsTabWidget.redirectCheck.setChecked(redirectEnabled)
        self.settingsTabWidget.installerCheck.setChecked(installerEnabled)
        self.settingsTabWidget.hashCheck.setChecked(hashEnabled)
        modeText = "Info"
        if loglevel == 0:
            modeText = "Debug"
        elif loglevel == 1:
            modeText = "Info"
        elif loglevel == 2:
            modeText = "Warning"
        elif loglevel == 3:
            modeText = "Critical"
        self.settingsTabWidget.debugLevelCombo.setCurrentText(modeText)

    def bindModeTabs(self):
        """Binds the mode and custom mode tabs."""
        linkFiles = self._rootBuilder._settings.linkfiles()
        copyFiles = self._rootBuilder._settings.copyfiles()
        usvfsFiles = self._rootBuilder._settings.usvfsfiles()
        linkPriority = self._rootBuilder._settings.linkpriority()
        copyPriority = self._rootBuilder._settings.copypriority()
        usvfsPriority = self._rootBuilder._settings.usvfspriority()
        noBuild = not self._rootBuilder._data.dataFileExists()

        linkModeOn = len(linkFiles) == 1 and linkFiles[0] == "**"
        linkModeOff = len(linkFiles) == 1 and linkFiles[0] == ""
        copyModeOn = len(copyFiles) == 1 and copyFiles[0] == "**"
        copyModeOff = len(copyFiles) == 1 and copyFiles[0] == ""
        usvfsModeOn = len(usvfsFiles) == 1 and usvfsFiles[0] == "**"
        usvfsModeOff = len(usvfsFiles) == 1 and usvfsFiles[0] == ""
        usvfsLinkModeOn = len(linkFiles) == 2 and linkFiles[0] == "**\\*.exe" and linkFiles[1] == "**\*.dll"

        linkMode = linkModeOn and copyModeOff and usvfsModeOff
        copyMode = copyModeOn and linkModeOff and usvfsModeOff
        usvfsMode = usvfsModeOn and copyModeOff and linkModeOff
        usvfsLinkMode = usvfsModeOn and usvfsLinkModeOn and copyModeOff 
        customMode = not linkMode and not copyMode and not usvfsMode and not usvfsLinkMode

        self.modeTabWidget.linkModeRadio.setEnabled(noBuild)
        self.modeTabWidget.copyModeRadio.setEnabled(noBuild)
        self.modeTabWidget.usvfsModeRadio.setEnabled(noBuild)
        self.modeTabWidget.usvfsLinkModeRadio.setEnabled(noBuild)
        self.modeTabWidget.customModeRadio.setEnabled(noBuild)

        self.modeTabWidget.linkModeRadio.setChecked(False)
        self.modeTabWidget.copyModeRadio.setChecked(False)
        self.modeTabWidget.usvfsModeRadio.setChecked(False)
        self.modeTabWidget.usvfsLinkModeRadio.setChecked(False)
        self.modeTabWidget.customModeRadio.setChecked(False)
        if linkMode:
            self.modeTabWidget.linkModeRadio.setChecked(True)
        elif copyMode:
            self.modeTabWidget.copyModeRadio.setChecked(True)
        elif usvfsMode:
            self.modeTabWidget.usvfsModeRadio.setChecked(True)
        elif usvfsLinkMode:
            self.modeTabWidget.usvfsLinkModeRadio.setChecked(True)
        else:
            self.modeTabWidget.customModeRadio.setChecked(True)

        self.customTabWidget.copyModePrioritySpin.setEnabled(noBuild)
        self.customTabWidget.linkModePrioritySpin.setEnabled(noBuild)
        self.customTabWidget.usvfsModePrioritySpin.setEnabled(noBuild)

        self.customTabWidget.copyModePrioritySpin.setValue(copyPriority)
        self.customTabWidget.linkModePrioritySpin.setValue(linkPriority)
        self.customTabWidget.usvfsModePrioritySpin.setValue(usvfsPriority)

    def bindModeWhitelistTables(self):
        """Binds the custom tables for different modes."""
        copyModeFiles = self._rootBuilder._settings.copyfiles()
        linkModeFiles = self._rootBuilder._settings.linkfiles()
        usvfsModeFiles = self._rootBuilder._settings.usvfsfiles()
        noBuild = not self._rootBuilder._data.dataFileExists()

        while "" in copyModeFiles:
            copyModeFiles.remove("")
        while "" in linkModeFiles:
            linkModeFiles.remove("")
        while "" in usvfsModeFiles:
            usvfsModeFiles.remove("")
        
        self.customTabWidget.copyModeTable.clear()
        self.customTabWidget.copyModeTable.setColumnCount(1)
        self.customTabWidget.copyModeTable.setRowCount(len(copyModeFiles) + 1)
        rows = 0
        for file in copyModeFiles:
            tableItem = QtWidgets.QTableWidgetItem(file)
            self.customTabWidget.copyModeTable.setItem(rows-1,1,tableItem)
            rows = rows + 1

        self.customTabWidget.linkModeTable.clear()
        self.customTabWidget.linkModeTable.setColumnCount(1)
        self.customTabWidget.linkModeTable.setRowCount(len(linkModeFiles) + 1)
        rows = 0
        for file in linkModeFiles:
            tableItem = QtWidgets.QTableWidgetItem(file)
            self.customTabWidget.linkModeTable.setItem(rows-1,1,tableItem)
            rows = rows + 1

        self.customTabWidget.usvfsModeTable.clear()
        self.customTabWidget.usvfsModeTable.setColumnCount(1)
        self.customTabWidget.usvfsModeTable.setRowCount(len(usvfsModeFiles) + 1)
        rows = 0
        for file in usvfsModeFiles:
            tableItem = QtWidgets.QTableWidgetItem(file)
            self.customTabWidget.usvfsModeTable.setItem(rows-1,1,tableItem)
            rows = rows + 1

        self.customTabWidget.copyModeTable.setEnabled(noBuild)
        self.customTabWidget.linkModeTable.setEnabled(noBuild)
        self.customTabWidget.usvfsModeTable.setEnabled(noBuild)

    def bindActionButtons(self):
        """Binds the buttons for different actions."""
        hasBuild = self._rootBuilder._data.dataFileExists()
        hasBackup = self._rootBuilder._backup.backupExists()
        hasCache = self._rootBuilder._cache.cacheFileExists()
        backupEnabled = self._rootBuilder._settings.backup()
        cacheEnabled = self._rootBuilder._settings.cache()
        noBuild = not hasBuild

        self.actionsTabWidget.syncButton.setEnabled(hasBuild)
        self.actionsTabWidget.clearButton.setEnabled(hasBuild)
        self.actionsTabWidget.buildButton.setEnabled(noBuild)

        self.actionsTabWidget.backupCreateButton.setEnabled(noBuild and backupEnabled and not hasBackup)
        self.actionsTabWidget.backupDeleteButton.setEnabled(noBuild and backupEnabled and hasBackup)

        self.actionsTabWidget.cacheCreateButton.setEnabled(noBuild and cacheEnabled and not hasCache)
        self.actionsTabWidget.cacheDeleteButton.setEnabled(noBuild and cacheEnabled and hasCache)

    def bindExclusionsTable(self):
        excludeFiles = self._rootBuilder._settings.exclusions()
        noBuild = not self._rootBuilder._data.dataFileExists()
        while "" in excludeFiles:
            excludeFiles.remove("")

        self.exclusionsTabWidget.exclusionsTable.setEnabled(noBuild)
        self.exclusionsTabWidget.exclusionsTable.clear()
        self.exclusionsTabWidget.exclusionsTable.setColumnCount(1)
        self.exclusionsTabWidget.exclusionsTable.setRowCount(len(excludeFiles) + 1)
        rows = 0
        for file in excludeFiles:
            tableItem = QtWidgets.QTableWidgetItem(file)
            self.exclusionsTabWidget.exclusionsTable.setItem(rows-1,1,tableItem)
            rows = rows + 1

    def copyModeButton_clicked(self):
        """Runs when the user switches to copy mode."""
        self._rootBuilder._settings.updateSetting("copyfiles", "**")
        self._rootBuilder._settings.updateSetting("linkfiles", "")
        self._rootBuilder._settings.updateSetting("usvfsfiles", "")
        self._rootBuilder._settings.updateSetting("usvfspriority", 3)
        self._rootBuilder._settings.updateSetting("linkpriority", 2)
        self._rootBuilder._settings.updateSetting("copypriority", 1)
        self.rebind()

    def linkModeButton_clicked(self):
        """Runs when the user switches to link mode."""
        self._rootBuilder._settings.updateSetting("linkfiles", "**")
        self._rootBuilder._settings.updateSetting("copyfiles", "")
        self._rootBuilder._settings.updateSetting("usvfsfiles", "")
        self._rootBuilder._settings.updateSetting("usvfspriority", 3)
        self._rootBuilder._settings.updateSetting("linkpriority", 2)
        self._rootBuilder._settings.updateSetting("copypriority", 1)
        self.rebind()

    def usvfsModeButton_clicked(self):
        """Runs when the user switches to usvfs mode."""
        self._rootBuilder._settings.updateSetting("usvfsfiles", "**")
        self._rootBuilder._settings.updateSetting("linkfiles", "")
        self._rootBuilder._settings.updateSetting("copyfiles", "")
        self._rootBuilder._settings.updateSetting("usvfspriority", 3)
        self._rootBuilder._settings.updateSetting("linkpriority", 2)
        self._rootBuilder._settings.updateSetting("copypriority", 1)
        self.rebind()

    def usvfslinkModeButton_clicked(self):
        """Runs when the user switches to usvfs + link mode."""
        self._rootBuilder._settings.updateSetting("usvfsfiles", "**")
        self._rootBuilder._settings.updateSetting("linkfiles", "**\\*.exe,**\\*.dll")
        self._rootBuilder._settings.updateSetting("copyfiles", "")
        self._rootBuilder._settings.updateSetting("usvfspriority", 3)
        self._rootBuilder._settings.updateSetting("linkpriority", 2)
        self._rootBuilder._settings.updateSetting("copypriority", 1)
        self.rebind()

    def customModeButton_clicked(self):
        """Runs when the user switches to custom mode."""
        self.modeTabWidget.linkModeRadio.setChecked(False)
        self.modeTabWidget.copyModeRadio.setChecked(False)
        self.modeTabWidget.usvfsModeRadio.setChecked(False)
        self.modeTabWidget.usvfsLinkModeRadio.setChecked(False)

    def copyModePrioritySpin_changed(self):
        """When the priority of copy mode is changed."""
        if not self._rebind:
            copyPriority = self._rootBuilder._settings.copypriority()
            linkPriority = self._rootBuilder._settings.linkpriority()
            usvfsPriority = self._rootBuilder._settings.usvfspriority()
            newPriority = self.customTabWidget.copyModePrioritySpin.value()
            if newPriority == linkPriority:
                self._rootBuilder._settings.updateSetting("copypriority", linkPriority)
                self._rootBuilder._settings.updateSetting("linkpriority", copyPriority)
            elif newPriority == usvfsPriority:
                self._rootBuilder._settings.updateSetting("copypriority", usvfsPriority)
                self._rootBuilder._settings.updateSetting("usvfspriority", copyPriority)
            self.rebind()

    def linkModePrioritySpin_changed(self):
        """When the priority of link mode is changed."""
        if not self._rebind:
            copyPriority = self._rootBuilder._settings.copypriority()
            linkPriority = self._rootBuilder._settings.linkpriority()
            usvfsPriority = self._rootBuilder._settings.usvfspriority()
            newPriority = self.customTabWidget.linkModePrioritySpin.value()
            if newPriority == copyPriority:
                self._rootBuilder._settings.updateSetting("copypriority", linkPriority)
                self._rootBuilder._settings.updateSetting("linkpriority", copyPriority)
            elif newPriority == usvfsPriority:
                self._rootBuilder._settings.updateSetting("linkpriority", usvfsPriority)
                self._rootBuilder._settings.updateSetting("usvfspriority", linkPriority)
            self.rebind()

    def usvfsModePrioritySpin_changed(self):
        """When the priority of usvfs mode is changed."""
        if not self._rebind:
            copyPriority = self._rootBuilder._settings.copypriority()
            linkPriority = self._rootBuilder._settings.linkpriority()
            usvfsPriority = self._rootBuilder._settings.usvfspriority()
            newPriority = self.customTabWidget.usvfsModePrioritySpin.value()
            if newPriority == copyPriority:
                self._rootBuilder._settings.updateSetting("copypriority", usvfsPriority)
                self._rootBuilder._settings.updateSetting("usvfspriority", copyPriority)
            elif newPriority == linkPriority:
                self._rootBuilder._settings.updateSetting("linkpriority", usvfsPriority)
                self._rootBuilder._settings.updateSetting("usvfspriority", linkPriority)
            self.rebind()

    def copyModeTable_cellChanged(self):
        """When a cell is edited on the copy mode table."""
        if not self._rebind:
            rows = self.customTabWidget.copyModeTable.rowCount()
            row = 0
            tableEntries = []
            while row <= rows:
                tableCell = self.customTabWidget.copyModeTable.item(row-1, 0)
                if tableCell:
                    cellText = tableCell.text()
                    tableEntries.append(cellText)
                row = row + 1
            newValue = ','.join(tableEntries)
            self._rootBuilder._settings.updateSetting("copyfiles", newValue)
            self.rebind()

    def linkModeTable_cellChanged(self):
        """When a cell is edited on the link mode table."""
        if not self._rebind:
            rows = self.customTabWidget.linkModeTable.rowCount()
            row = 0
            tableEntries = []
            while row <= rows:
                tableCell = self.customTabWidget.linkModeTable.item(row-1, 0)
                if tableCell:
                    cellText = tableCell.text()
                    tableEntries.append(cellText)
                row = row + 1
            newValue = ','.join(tableEntries)
            self._rootBuilder._settings.updateSetting("linkfiles", newValue)
            self.rebind()

    def usvfsModeTable_cellChanged(self):
        """When a cell is edited on the usvfs mode table."""
        if not self._rebind:
            rows = self.customTabWidget.usvfsModeTable.rowCount()
            row = 0
            tableEntries = []
            while row <= rows:
                tableCell = self.customTabWidget.usvfsModeTable.item(row-1, 0)
                if tableCell:
                    cellText = tableCell.text()
                    tableEntries.append(cellText)
                row = row + 1
            newValue = ','.join(tableEntries)
            self._rootBuilder._settings.updateSetting("usvfsfiles", newValue)
            self.rebind()

    def exclusionsTable_cellChanged(self):
        """When a cell is edited on the exclusionstable."""
        if not self._rebind:
            rows = self.exclusionsTabWidget.exclusionsTable.rowCount()
            row = 0
            tableEntries = []
            while row <= rows:
                tableCell = self.exclusionsTabWidget.exclusionsTable.item(row-1, 0)
                if tableCell:
                    cellText = tableCell.text()
                    tableEntries.append(cellText)
                row = row + 1
            newValue = ','.join(tableEntries)
            self._rootBuilder._settings.updateSetting("exclusions", newValue)
            self.rebind()

    def backupCheck_changed(self):
        """When backup is enabled/disabled."""
        if not self._rebind:
            enabled = self.settingsTabWidget.backupCheck.isChecked()
            self._rootBuilder._settings.updateSetting("backup", enabled)
            if not enabled:
                self._rootBuilder._backup.deleteBackup()
            self.rebind()    

    def cacheCheck_changed(self):
        """When cache is enabled/disabled."""
        if not self._rebind:
            enabled = self.settingsTabWidget.cacheCheck.isChecked()
            self._rootBuilder._settings.updateSetting("cache", enabled)
            if not enabled:
                self._rootBuilder._cache.deleteCacheFile()
            self.rebind()    

    def hashCheck_changed(self):
        """When hashing is enabled/disabled."""
        if not self._rebind:
            enabled = self.settingsTabWidget.hashCheck.isChecked()
            self._rootBuilder._settings.updateSetting("hash", enabled)

    def autobuildCheck_changed(self):
        """When autobuild is enabled/disabled."""
        if not self._rebind:
            enabled = self.settingsTabWidget.autobuildCheck.isChecked()
            self._rootBuilder._settings.updateSetting("autobuild", enabled)

    def redirectCheck_changed(self):
        """When redirect is enabled/disabled."""
        if not self._rebind:
            enabled = self.settingsTabWidget.redirectCheck.isChecked()
            self._rootBuilder._settings.updateSetting("redirect", enabled)

    def installerCheck_changed(self):
        """When installer is enabled/disabled."""
        if not self._rebind:
            enabled = self.settingsTabWidget.installerCheck.isChecked()
            self._rootBuilder._settings.updateSetting("installer", enabled)

    def debugModeCombo_changed(self):
        """When debug mode changes."""
        if not self._rebind:
            newMode = self.settingsTabWidget.debugLevelCombo.currentText()
            newLevel = 1
            if newMode == "Debug":
                newLevel = 0
            elif newMode == "Info":
                newLevel = 1
            elif newMode == "Warning":
                newLevel = 2
            elif newMode == "Critical":
                newLevel = 3
            self._rootBuilder._settings.updateSetting("loglevel", newLevel)

    def deleteBackup_clicked(self):
        self._rootBuilder._backup.deleteBackup()
        self.rebind()

    def deleteCache_clicked(self):
        self._rootBuilder._cache.deleteCacheFile()
        self.rebind()

    def createBackup_clicked(self):
        self._rootBuilder._backup.updateBackup(True)
        self.rebind()

    def createCache_clicked(self):
        newCache = self._rootBuilder._cache.updateCache()
        self._rootBuilder._cache.saveCacheFile(newCache)
        self.rebind()

    def build_clicked(self):
        self._rootBuilder.build()
        self.rebind()

    def sync_clicked(self):
        self._rootBuilder.sync()
        self.rebind()

    def clear_clicked(self):
        self._rootBuilder.clear()
        self.rebind()

    def discord_clicked(self):
        webbrowser.open("https://discord.com/invite/kPA3RrxAYz")

    def docs_clicked(self):
        webbrowser.open("https://kezyma.github.io/?p=rootbuilder")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/31720")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")

    def updateFound_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/31720?tab=files")
       
    def checkUpdate_clicked(self):
        """Checks for an update"""
        newVersion = self._update.getLatestVersion()
        hasUpdate = newVersion != None
        self.updateTabWidget.updateFoundWidget.setVisible(hasUpdate)
        self.updateTabWidget.noUpdateWidget.setVisible(not hasUpdate)

    def exportButton_clicked(self):
        """Exports the current settings file."""
        fileDialog = QtWidgets.QFileDialog()
        if fileDialog.exec():
            filePath = fileDialog.selectedFiles()[0]
            self._rootBuilder._export.exportSettings(filePath)
            self.rebind()

    def importButton_clicked(self):
        fileDialog = QtWidgets.QFileDialog()
        if fileDialog.exec():
            filePath = fileDialog.selectedFiles()[0]
            self._rootBuilder._export.importSettings(filePath)
            self.rebind()

    def resetButton_clicked(self):
        self._rootBuilder._export.resetSettings()
        self.rebind()