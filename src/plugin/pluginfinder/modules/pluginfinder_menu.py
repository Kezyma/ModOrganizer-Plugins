from ....common.common_icons import CommonIcons
from ....common.common_qt import *
from ..core.pluginfinder import PluginFinder
#from .profilesync_update import ProfileSyncUpdate
import mobase, webbrowser, os
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

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, pluginFinder:PluginFinder):
        super().__init__(parent)
        self._organiser = organiser
        self._pluginFinder = pluginFinder
        #self._update = update
        self._rebind = False
        self._icons = CommonIcons()
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_pluginFinderMenuWidget()
        self.widget.setupUi(self)

        self.finderTabWidget = Ui_listTabWidget()
        self.finderTabWidget.setupUi(self.widget.finderTab)
        self.finderTabWidget.refreshButton.setIcon(self._icons.refreshIcon())
        self.finderTabWidget.refreshButton.clicked.connect(self.refresh_clicked)

        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

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

        self.finderTabWidget.searchText.textChanged.connect(self.rebind)
        self.finderTabWidget.updateCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.installedCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.supportedCheck.stateChanged.connect(self.rebind)
        self.finderTabWidget.workingCheck.stateChanged.connect(self.rebind)

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
                                                                     self.finderTabWidget.workingCheck.isChecked()) #self._pluginFinder._directory.loadManifests()
        self._installData = self._pluginFinder._install.loadInstallData()
        self._pluginListItems = {}

        for i in reversed(range(self.finderTabWidget.pluginListLayout.count())): 
            self.finderTabWidget.pluginListLayout.itemAt(i).widget().setParent(None)

        for key in self._manifests.keys():
            self._pluginListItems[key] = self.getPluginWidget(key)
       
    def getPluginWidget(self, pluginId:str) -> QtWidgets.QWidget:
        manifest = self._manifests[pluginId]
        latestVersion = self._pluginFinder._directory.getLatestVersion(pluginId)
        
        listWidget = QtWidgets.QWidget()
        listItem = Ui_pluginItemWidget()
        listItem.setupUi(listWidget)
        pluginId = str(pluginId)
        listItem.pluginNameText.setText(manifest[self._pluginFinder._directory.NAME])
        listItem.installedVersionLabel.setText("")
        listItem.currentVersionLabel.setText(f"Latest: {latestVersion.displayString()}")
        listItem.authorLabel.setText(f"by {manifest[self._pluginFinder._directory.AUTHOR]}")
        listItem.descriptionText.setText(manifest[self._pluginFinder._directory.DESCRIPTION])

        # Bind external links.
        listItem.githubButton.setIcon(self._icons.githubIcon())
        if self._pluginFinder._directory.GITHUB in manifest and manifest[self._pluginFinder._directory.GITHUB] != "":
            githubUrl = str(manifest[self._pluginFinder._directory.GITHUB])
            listItem.githubButton.clicked.connect(lambda: webbrowser.open(githubUrl))
        else:
            listItem.githubButton.setEnabled(False)

        listItem.nexusButton.setIcon(self._icons.nexusIcon())
        if self._pluginFinder._directory.NEXUS in manifest and manifest[self._pluginFinder._directory.NEXUS] != "":
            nexusUrl = str(manifest[self._pluginFinder._directory.NEXUS])
            listItem.nexusButton.clicked.connect(lambda: webbrowser.open(nexusUrl))
        else:
            listItem.nexusButton.setEnabled(False)

        listItem.docsButton.setIcon(self._icons.docsIcon())
        if self._pluginFinder._directory.DOCS in manifest and manifest[self._pluginFinder._directory.DOCS] != "":
            docsUrl = str(manifest[self._pluginFinder._directory.DOCS])
            listItem.docsButton.clicked.connect(lambda: webbrowser.open(docsUrl))
        else:
            listItem.docsButton.setEnabled(False)

        # Install and Uninstall buttons.
        installed = self._pluginFinder._search.pluginInstalled(pluginId)
        needsUpdate = self._pluginFinder._search.pluginNeedsUpdate(pluginId)
        supported = self._pluginFinder._search.pluginIsSupported(pluginId)
        working = self._pluginFinder._search.pluginIsWorking(pluginId)
        isPluginFinder = pluginId == "pluginfinder"
        if not working:
            listItem.installButton.setEnabled(False)
            listItem.installButton.setToolTip("Unsupported")
            if needsUpdate:
                listItem.installButton.setIcon(self._icons.noUpdateIcon())
            else:
                listItem.installButton.setIcon(self._icons.stopIcon())
        elif needsUpdate:
            if supported:
                listItem.installButton.setToolTip("Update Available")
                listItem.installButton.setIcon(self._icons.updateIcon())
            else:
                listItem.installButton.setToolTip("Update; this update may not work on this version of Mod Organizer.")
                listItem.installButton.setIcon(self._icons.updateAltIcon())
        elif installed:
            listItem.installButton.setToolTip("Installed")
            listItem.installButton.setIcon(self._icons.checkIcon())
            listItem.installButton.setEnabled(False)
        else:
            if supported:
                listItem.installButton.setToolTip("Install")
                listItem.installButton.setIcon(self._icons.installIcon())
            else:
                listItem.installButton.setToolTip("Install; this plugin may not work on this version of Mod Organizer.")
                listItem.installButton.setIcon(self._icons.warningIcon())
        listItem.installButton.clicked.connect(lambda: self.install_clicked(pluginId))
        listItem.uninstallButton.clicked.connect(lambda: self.uninstall_clicked(pluginId))

        listItem.uninstallButton.setToolTip("Uninstall")
        listItem.uninstallButton.setEnabled(installed and not isPluginFinder)
        listItem.uninstallButton.setIcon(self._icons.trashIcon())

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
        webbrowser.open("https://kezyma.github.io/?p=pluginfinder")

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
