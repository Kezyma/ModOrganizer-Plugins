from typing import Tuple, Union
import mobase, threading

from mobase import GuessedString, IFileTree, IModInterface, InstallResult
from ..core.pluginfinder_plugin import PluginFinderPlugin
from ..modules.pluginfinder_menu import PluginFinderMenu
try:
    from ..ui.qt6.pluginfinder_install import Ui_installDialogMenu
except:
    from ..ui.qt5.pluginfinder_install import Ui_installDialogMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *
from ..models.pluginfinder_installdata import *
from ..models.pluginfinder_manifestdata import *
from ..models.pluginfinder_versiondata import *

class PluginFinderInstaller(PluginFinderPlugin, mobase.IPluginInstallerSimple):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return LINK_ALT_ICON

    def name(self):
        return f"{self.baseName()} Installer"

    def displayName(self):
        return f"{self.baseDisplayName()} Installer"

    def description(self):
        return self.__tr("Installs plugins downloaded to Mod Organizer.")
    
    def settings(self):
        return []
    
    def master(self):
        return self.baseName()
    
    def priority(self) -> int:
        return self._pluginFinder._settings.priority()

    def isManualInstaller(self) -> bool:
        return False

    def isArchiveSupported(self, tree: IFileTree) -> bool:
        self._log.info(f"Checking for Mod Organizer plugin.")
        res = self._pluginFinder._install.treeIsPlugin(tree)
        if res:
            self._log.info("Found Mod Organizer plugin.")
        else:
            self._log.info("No Mod Organizer plugin found.")
        return res
    
    _archiveFile = None
    def onInstallationStart(self, archive: str, reinstallation: bool, current_mod: IModInterface):
        self._archiveFile = archive

    def install(self, name: GuessedString, tree: IFileTree, version: str, nexus_id: int) -> Union[InstallResult, IFileTree, Tuple[InstallResult, IFileTree, str, int]]:
        self._install.pluginNameText.setText(self._pluginFinder._install.manualPluginName())
        res = self._dialog.exec()
        if res == qDialogCode.Rejected:
            if self._manualRequest:
                return mobase.InstallResult.MANUAL_REQUESTED
            else:
                return mobase.InstallResult.CANCELED
        elif res == qDialogCode.Accepted:
            self._pluginFinder._install.installFromFile(self._archiveFile)
            self._pluginFinder._install.reloadData()
            return mobase.InstallResult.CANCELED
        else:
            return mobase.InstallResult.NOT_ATTEMPTED

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), f"v{self.version().displayString()}", self.icon())
        self._installWidget = QtWidgets.QWidget(dialog)
        self._install = Ui_installDialogMenu() 
        self._install.setupUi(self._installWidget)
        dialog.addContent(self._installWidget)
        
        self._install.installBtn.clicked.connect(self.install_clicked)
        self._install.cancelBtn.clicked.connect(self.cancel_clicked)
        self._install.manualBtn.clicked.connect(self.manual_clicked)
        return dialog

    def install_clicked(self):
        self._dialog.accept()

    _manualRequest = False
    def cancel_clicked(self):
        self._manualRequest = False
        self._dialog.reject()

    def manual_clicked(self):
        self._manualRequest = True
        self._dialog.reject()