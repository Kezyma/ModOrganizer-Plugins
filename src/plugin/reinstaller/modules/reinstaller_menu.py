import mobase, webbrowser
from pathlib import Path
try:
    from ..ui.qt6.reinstaller_menu import Ui_reinstallerMenu
    from ..ui.qt6.reinstaller_installers import Ui_reinstallerInstallers
    from ....base.ui.qt6.update_widget import Ui_updateTabWidget
except:
    from ..ui.qt5.reinstaller_menu import Ui_reinstallerMenu
    from ..ui.qt5.reinstaller_installers import Ui_reinstallerInstallers
    from ....base.ui.qt5.update_widget import Ui_updateTabWidget

from ..core.reinstaller import Reinstaller
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ....common.common_icons import *
from ....common.common_qt import *

class ReinstallerMenu(QtWidgets.QWidget):
    """Reinstaller create widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, reinstaller:Reinstaller, update:CommonUpdate, help:CommonHelp):
        super().__init__(parent)
        self._organiser = organiser
        self._reinstaller = reinstaller
        self._update = update
        self._help = help
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

        self._update.configure(self.updateTabWidget)
        self._help.configure(self.helpTabWidget)
        
        self.installersTabWidget.txtName.textChanged.connect(self.txtNameChange)
        self.installersTabWidget.ddlDownloads.currentTextChanged.connect(self.ddlDownloadChange)
        self.installersTabWidget.btnAdd.clicked.connect(self.btnAddClick)
        self.installersTabWidget.lstInstallers.currentItemChanged.connect(self.lstInstallersChange)
        self.installersTabWidget.btnInstall.clicked.connect(self.btnInstallClick)
        self.installersTabWidget.btnDelete.clicked.connect(self.btnDeleteClick)

        self.installersTabWidget.btnAdd.setIcon(PLUS_ICON)
        self.installersTabWidget.btnInstall.setIcon(INSTALL_ICON)
        self.installersTabWidget.btnDelete.setIcon(TRASH_ICON)

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
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/reinstaller.md")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/59292")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")
