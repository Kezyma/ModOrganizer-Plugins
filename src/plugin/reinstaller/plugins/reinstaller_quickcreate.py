import mobase, os
from pathlib import Path
from ..core.reinstaller_plugin import ReinstallerPlugin
from ..modules.reinstaller_menu import ReinstallerMenu
from ..modules.reinstaller_update import ReinstallerUpdate
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import PLUS_ICON

class ReinstallerQuickCreate(ReinstallerPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._update = ReinstallerUpdate(self._organiser, self, self._reinstaller._strings, self._reinstaller._log)
        self.dialog = QtWidgets.QWidget()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self.baseName()

    def icon(self):
        return PLUS_ICON
    
    def settings(self):
        return []

    def name(self):
        return self.baseName() + " Create Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Create"

    def description(self):
        return self.__tr("Creates a new installer from a downloaded file.")

    def display(self):
        modFiles = self._reinstaller._paths.getDownloadFileOptions()
        item, ok = QInputDialog.getItem(self.dialog, "Select Installer", "Installer:", modFiles, 0, False)
        if ok and item:
            name, ok = QInputDialog.getText(self.dialog, "Name", "Installer Name:", qEchoMode.Normal, self._reinstaller._paths.getDownloadFileName(str(item)))
            if ok and name:
                self._reinstaller.create(str(name), str(item))

