from ....common.common_icons import *
from ....common.common_qt import *
from ....common.common_help import CommonHelp
from ..core.pluginfinder import PluginFinder
import mobase, webbrowser, os
from ..models.pluginfinder_versiondata import *
from ..models.pluginfinder_manifestdata import *
from ..models.pluginfinder_directorydata import *
from ..models.pluginfinder_installdata import *
from pathlib import Path

try:
    from ..ui.qt6.pluginfinder_menu import Ui_pluginFinderMenuWidget
    from ..ui.qt6.pluginfinder_list import Ui_listTabWidget
    from ..ui.qt6.pluginfinder_item import Ui_pluginItemWidget
except:
    from ..ui.qt5.pluginfinder_menu import Ui_pluginFinderMenuWidget
    from ..ui.qt5.pluginfinder_list import Ui_listTabWidget
    from ..ui.qt5.pluginfinder_item import Ui_pluginItemWidget

class PluginFinderMenu(QtWidgets.QWidget):
    """Plugin Finder menu widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, pluginFinder:PluginFinder, help:CommonHelp):
        super().__init__(parent)
        self._organiser = organiser
        self._pluginFinder = pluginFinder
        self._help = help
        self._rebind = False
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_pluginFinderMenuWidget()
        self.widget.setupUi(self)

        self.finderTabWidget = Ui_listTabWidget()
        self.finderTabWidget.setupUi(self.widget.finderTab)
        self.finderTabWidget.refreshButton.setIcon(REFRESH_ICON)
        self.finderTabWidget.refreshButton.clicked.connect(self.refresh_clicked)

        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)
        self._help.configure(self.helpTabWidget)

        self.finderTabWidget.searchText.textChanged.connect(self.rebind)
        self.finderTabWidget.updateCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.installedCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.supportedCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.workingCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.directionCombo.currentTextChanged.connect(self.rebind)
        self.finderTabWidget.sortCombo.currentTextChanged.connect(self.rebind)

    def rebind(self):
        self.bindPluginList()

    _pluginListItems = {}
    _manifests = {}
    _installData = {}
    def bindPluginList(self):
        self._manifests = self._pluginFinder._search.searchDirectory(self.finderTabWidget.searchText.text(), 
                                                                     self.finderTabWidget.installedCheck.isChecked(), 
                                                                     self.finderTabWidget.updateCheck.isChecked(), 
                                                                     self.finderTabWidget.supportedCheck.isChecked(),
                                                                     self.finderTabWidget.workingCheck.isChecked(),
                                                                     self.finderTabWidget.sortCombo.currentText(),
                                                                     self.finderTabWidget.directionCombo.currentText()) #self._pluginFinder._directory.loadManifests()
        self._installData = self._pluginFinder._install.loadInstallData()
        self._pluginListItems = {}

        for i in reversed(range(self.finderTabWidget.pluginListLayout.count())): 
            self.finderTabWidget.pluginListLayout.itemAt(i).widget().setParent(None)

        for key in self._manifests.keys():
            self._pluginListItems[key] = self.getPluginWidget(key)
       
    def getPluginWidget(self, pluginId:str) -> QtWidgets.QWidget:
        manifest = self._manifests[pluginId]
        latestVersion = self._pluginFinder._directory.getLatestVersion(pluginId)
        installed = self._pluginFinder._search.pluginInstalled(pluginId)
        
        listWidget = QtWidgets.QWidget()
        listItem = Ui_pluginItemWidget()
        listItem.setupUi(listWidget)
        pluginId = str(pluginId)
        listItem.pluginNameText.setText(manifest[NAME])
        listItem.installedVersionLabel.setText("")
        if installed:
            instVer = mobase.VersionInfo(self._installData[pluginId][VERSION])
            listItem.installedVersionLabel.setText(f"Installed: {instVer.displayString()}")
        listItem.currentVersionLabel.setText(f"Latest: {latestVersion.displayString()}")
        listItem.authorLabel.setText(f"by {manifest[AUTHOR]}")
        listItem.descriptionText.setText(manifest[DESCRIPTION])

        # Bind external links.
        listItem.githubButton.setIcon(GITHUB_ICON)
        if GITHUBURL in manifest and manifest[GITHUBURL] != "":
            githubUrl = str(manifest[GITHUBURL])
            listItem.githubButton.clicked.connect(lambda: webbrowser.open(githubUrl))
        else:
            listItem.githubButton.setEnabled(False)

        listItem.nexusButton.setIcon(NEXUS_ICON)
        if NEXUSURL in manifest and manifest[NEXUSURL] != "":
            nexusUrl = str(manifest[NEXUSURL])
            listItem.nexusButton.clicked.connect(lambda: webbrowser.open(nexusUrl))
        else:
            listItem.nexusButton.setEnabled(False)

        listItem.docsButton.setIcon(DOCS_ICON)
        if DOCSURL in manifest and manifest[DOCSURL] != "":
            docsUrl = str(manifest[DOCSURL])
            listItem.docsButton.clicked.connect(lambda: webbrowser.open(docsUrl))
        else:
            listItem.docsButton.setEnabled(False)

        # Install and Uninstall buttons.
        needsUpdate = self._pluginFinder._search.pluginNeedsUpdate(pluginId)
        supported = self._pluginFinder._search.pluginIsSupported(pluginId)
        working = self._pluginFinder._search.pluginIsWorking(pluginId)
        isPluginFinder = pluginId == "pluginfinder"
        if not working:
            listItem.installButton.setEnabled(False)
            listItem.installButton.setToolTip("Unsupported")
            if needsUpdate:
                listItem.installButton.setIcon(NO_UPDATE_ICON)
            else:
                listItem.installButton.setIcon(STOP_ICON)
        elif needsUpdate:
            if supported:
                listItem.installButton.setToolTip("Update Available")
                listItem.installButton.setIcon(UPDATE_ICON)
            else:
                listItem.installButton.setToolTip("Update; this update may not work on this version of Mod Organizer.")
                listItem.installButton.setIcon(UPDATE_ALT_ICON)
        elif installed:
            listItem.installButton.setToolTip("Installed")
            listItem.installButton.setIcon(CHECK_ICON)
            listItem.installButton.setEnabled(False)
        else:
            if supported:
                listItem.installButton.setToolTip("Install")
                listItem.installButton.setIcon(INSTALL_ICON)
            else:
                listItem.installButton.setToolTip("Install; this plugin may not work on this version of Mod Organizer.")
                listItem.installButton.setIcon(WARNING_ICON)
        listItem.installButton.clicked.connect(lambda: self.install_clicked(pluginId))
        listItem.uninstallButton.clicked.connect(lambda: self.uninstall_clicked(pluginId))

        listItem.uninstallButton.setToolTip("Uninstall")
        listItem.uninstallButton.setEnabled(installed and not isPluginFinder)
        listItem.uninstallButton.setIcon(TRASH_ICON)

        self.finderTabWidget.pluginListLayout.addWidget(listWidget)
        return listItem

    def install_clicked(self, pluginId:str):
        self._pluginFinder._install.installPlugin(pluginId)
        self.rebind()

    def uninstall_clicked(self, pluginId:str):
        self._pluginFinder._install.uninstallPlugin(pluginId)
        self.rebind()

    def discord_clicked(self):
        webbrowser.open("https://discord.com/invite/kPA3RrxAYz")

    def docs_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/pluginfinder.md")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/59869")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")

    def refresh_clicked(self):
        self._pluginFinder._directory.updateDirectory()
        self._pluginFinder._directory.loadManifests(True)
        self.bindPluginList()
