from typing import Tuple, Union
import mobase
from mobase import GuessedString, IFileTree, InstallResult
from ..core.rootbuilder_plugin import RootBuilderPlugin
from ..modules.rootbuilder_install import RootBuilderInstall
from ..modules.rootbuilder_update import RootBuilderUpdate
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *

class RootBuilderInstaller(RootBuilderPlugin, mobase.IPluginInstallerSimple):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self._pluginName
    
    def settings(self):
        return []

    def icon(self):
        return self._icons.linkAltIcon()

    def name(self):
        return self.baseName() + " Installer"

    def displayName(self):
        return self.baseDisplayName() + " Installer"

    def description(self):
        return self.__tr("Installs Root mods.")
    
    def isArchiveSupported(self, tree: IFileTree) -> bool:
        return self._rootBuilder._settings.installer() and self._install.isRootMod(tree)

    def isManualInstaller(self) -> bool:
        return False
    
    def priority(self) -> int:
        return self._rootBuilder._settings.priority()
    
    def install(self, name: GuessedString, tree: IFileTree, version: str, nexus_id: int) -> Union[InstallResult, IFileTree, Tuple[InstallResult, IFileTree, str, int]]:
        self._install.widget.modNameCombo.clear()
        self._install.widget.modNameCombo.addItems(name.variants())
        self._install.widget.installBtn.clicked.connect(self.install_clicked)
        self._install.widget.cancelBtn.clicked.connect(self.cancel_clicked)
        self._install.widget.manualBtn.clicked.connect(self.manual_clicked)
        res = self._dialog.exec()
        if res == qDialogCode.Rejected:
            if self._manualRequest:
                return mobase.InstallResult.MANUAL_REQUESTED
            else:
                return mobase.InstallResult.CANCELED
        elif res == qDialogCode.Accepted:
            modtree = self._install.repackMod(tree)
            name.setFilter(self.retrieveName)
            name.update(self.retrieveName(""))
            return modtree
        else:
            return mobase.InstallResult.NOT_ATTEMPTED

    def display(self):
        self._dialog.show()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), "v" + self.version().displayString(), self.icon())
        self._install = RootBuilderInstall(dialog, self._organiser, self._rootBuilder._strings, self._rootBuilder._paths,  self._rootBuilder._util, self._log)
        dialog.addContent(self._install)
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

    def retrieveName(self, current:str):
        return self._install.widget.modNameCombo.currentText()