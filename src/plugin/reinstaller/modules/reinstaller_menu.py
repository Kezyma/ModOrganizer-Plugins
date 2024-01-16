import mobase, webbrowser
from pathlib import Path
try:
    from ..ui.qt6.reinstaller_menu import Ui_reinstallerMenu
    from ..ui.qt6.reinstaller_installers import Ui_reinstallerInstallers
    from ..ui.qt6.reinstaller_update import Ui_updateTabWidget
except:
    from ..ui.qt5.reinstaller_menu import Ui_reinstallerMenu
    from ..ui.qt5.reinstaller_installers import Ui_reinstallerInstallers
    from ..ui.qt5.reinstaller_update import Ui_updateTabWidget

from ..core.reinstaller import Reinstaller
from .reinstaller_update import ReinstallerUpdate
from ....common.common_icons import *
from ....common.common_qt import *

class ReinstallerMenu(QtWidgets.QWidget):
    """Reinstaller create widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, reinstaller:Reinstaller, update:ReinstallerUpdate):
        super().__init__(parent)
        self._organiser = organiser
        self._reinstaller = reinstaller
        self._update = update
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_reinstallerMenu()
        self.widget.setupUi(self)

        self.installersTabWidget = Ui_reinstallerInstallers()
        self.installersTabWidget.setupUi(self.widget.installersTab)

        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)

        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self.updateTabWidget.updateFoundWidget.setVisible(False)
        self.updateTabWidget.noUpdateWidget.setVisible(False)
        self.updateTabWidget.checkUpdateButton.setIcon(REFRESH_ICON)
        self.updateTabWidget.updateFoundButton.setIcon(DOWNLOAD_ICON)
        self.updateTabWidget.updateFoundButton.clicked.connect(self.updateFound_clicked)
        self.updateTabWidget.checkUpdateButton.clicked.connect(self.checkUpdate_clicked)

        self.helpTabWidget.discordButton.setIcon(DISCORD_ICON)
        self.helpTabWidget.discordButton.clicked.connect(self.discord_clicked)
        self.helpTabWidget.docsButton.setIcon(DOCS_ICON)
        self.helpTabWidget.docsButton.clicked.connect(self.docs_clicked)
        self.helpTabWidget.githubButton.setIcon(GITHUB_ICON)
        self.helpTabWidget.githubButton.clicked.connect(self.github_clicked)
        self.helpTabWidget.nexusButton.setIcon(NEXUS_ICON)
        self.helpTabWidget.nexusButton.clicked.connect(self.nexus_clicked)
        self.helpTabWidget.patreonButton.setIcon(PATREON_ICON)
        self.helpTabWidget.patreonButton.clicked.connect(self.patreon_clicked)

        helpPath = Path(__file__).parent.parent / "data" / "reinstaller_help.html"
        helpUrl = QtCore.QUrl.fromLocalFile(str(helpPath.absolute()))
        self.helpTabWidget.helpText.setSource(helpUrl)

        self.installersTabWidget.txtName.textChanged.connect(self.txtNameChange)
        self.installersTabWidget.ddlDownloads.currentTextChanged.connect(self.ddlDownloadChange)
        self.installersTabWidget.btnAdd.clicked.connect(self.btnAddClick)
        self.installersTabWidget.lstInstallers.currentItemChanged.connect(self.lstInstallersChange)
        self.installersTabWidget.btnInstall.clicked.connect(self.btnInstallClick)
        self.installersTabWidget.btnDelete.clicked.connect(self.btnDeleteClick)

    def rebind(self):
        self.installersTabWidget.ddlDownloads.clear()
        self.installersTabWidget.ddlDownloads.addItems(self._reinstaller._paths.getDownloadFileOptions())
        self.installersTabWidget.ddlInstaller.clear()
        self.installersTabWidget.lstInstallers.clear()
        self.installersTabWidget.lstInstallers.addItems(self._reinstaller._paths.getInstallerOptions())

    def txtNameChange(self):
        value = self.installersTabWidget.txtName.text().strip()
        if value:
            self.installersTabWidget.btnAdd.setEnabled(True)
        else:
            self.installersTabWidget.btnAdd.setEnabled(False)

    def ddlDownloadChange(self):
        value = self.installersTabWidget.ddlDownloads.currentText()
        if value:
            self.installersTabWidget.txtName.setEnabled(True)
            self.installersTabWidget.btnAdd.setEnabled(True)
            self.installersTabWidget.txtName.setText(self._reinstaller._paths.getDownloadFileName(value))
        else:
            self.installersTabWidget.txtName.setEnabled(False)
            self.installersTabWidget.btnAdd.setEnabled(False)

    def lstInstallersChange(self):
        item = self.installersTabWidget.lstInstallers.currentItem()
        self.installersTabWidget.ddlInstaller.clear()
        self.installersTabWidget.btnInstall.setEnabled(False)
        self.installersTabWidget.btnDelete.setEnabled(False)
        if item:
            fileOptions = self._reinstaller._paths.fileNames(self._reinstaller._paths.getInstallerFileOptions(item.text()))
            if len(fileOptions) > 0:
                self.installersTabWidget.ddlInstaller.addItems(fileOptions)
                self.installersTabWidget.btnInstall.setEnabled(True)
                self.installersTabWidget.btnDelete.setEnabled(True)

    def btnInstallClick(self):
        modName = self.installersTabWidget.lstInstallers.currentItem().text()
        modPath = self.installersTabWidget.ddlInstaller.currentText()
        self._reinstaller.install(str(modName), str(modPath))

    def btnDeleteClick(self):
        modName = self.installersTabWidget.lstInstallers.currentItem().text()
        modPath = self.installersTabWidget.ddlInstaller.currentText()
        name = self._reinstaller.delete(str(modName), str(modPath))
        self.rebind()

    def btnAddClick(self):
        self._reinstaller.create(self.installersTabWidget.txtName.text().strip(), self.installersTabWidget.ddlDownloads.currentText())
        self.rebind()

    def discord_clicked(self):
        webbrowser.open("https://discord.com/invite/kPA3RrxAYz")

    def docs_clicked(self):
        webbrowser.open("https://kezyma.github.io/?p=reinstaller")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/59292")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")

    def updateFound_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/59292?tab=files")
       
    def checkUpdate_clicked(self):
        """Checks for an update"""
        newVersion = self._update.getLatestVersion()
        hasUpdate = newVersion is not None
        self.updateTabWidget.updateFoundWidget.setVisible(hasUpdate)
        self.updateTabWidget.noUpdateWidget.setVisible(not hasUpdate)