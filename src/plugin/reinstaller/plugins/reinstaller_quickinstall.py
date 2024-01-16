import mobase, os
from pathlib import Path
from ..core.reinstaller_plugin import ReinstallerPlugin
from ..modules.reinstaller_menu import ReinstallerMenu
from ..modules.reinstaller_update import ReinstallerUpdate
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import CHECK_ICON

class ReinstallerQuickInstall(ReinstallerPlugin, mobase.IPluginTool):
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
        return CHECK_ICON
    
    def settings(self):
        return []

    def name(self):
        return self.baseName() + " Install Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Install"

    def description(self):
        return self.__tr("Runs an installer from a backed up file.")
    
    def display(self):
        item, ok = QInputDialog.getItem(self.dialog, "Run Installer", "Installer:", self._reinstaller._paths.getInstallerOptions(), 0, False)
        if ok and item:
            files = self._reinstaller._paths.getInstallerFileOptions(item) 
            if len(files) == 1:
                self._reinstaller.install(str(item), str(os.path.basename(str(files[0]))))
            if (len(files)) > 1:
                item2, ok = QInputDialog.getItem(self.dialog, "Select File", "File:", self._reinstaller._paths.fileNames(files), 0, False)
                if ok and item2:
                    self._reinstaller.install(str(item), str(item2))

