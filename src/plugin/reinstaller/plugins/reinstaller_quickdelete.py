import mobase, os
from pathlib import Path
from ..core.reinstaller_plugin import ReinstallerPlugin
from ..modules.reinstaller_menu import ReinstallerMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import MINUS_ICON


class ReinstallerQuickDelete(ReinstallerPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser: mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = QtWidgets.QWidget()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self.baseName()

    def icon(self):
        return MINUS_ICON

    def settings(self):
        return []

    def name(self):
        return self.baseName() + " Delete Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Delete"

    def description(self):
        return self.__tr("Deletes a downloaded file.")

    def display(self):
        if self._organiser.pluginSetting("Reinstaller", "copy_installers"):
            self._display()
        else:
            self._display_no_copy()

    def _display(self):
        installers = self._reinstaller._paths.subfolders(self._reinstaller._strings.pluginDataPath)
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))

        item, ok = QInputDialog.getItem(self.dialog, "Delete Installer", "Installer:", names, 0, False)
        if ok and item:
            installerOpts = self._reinstaller._paths.files(str(Path(self._reinstaller._strings.pluginDataPath) / item))
            files = []
            for file in installerOpts:
                if not str(file).endswith(".meta"):
                    files.append(file)
            if len(files) == 1:
                self._reinstaller.delete(item, os.path.basename(files[0]))
            if (len(files)) > 1:
                optionFiles = []
                for opt in files:
                    optionFiles.append(os.path.basename(opt))
                item2, ok = QInputDialog.getItem(self.dialog, "Delete File", "File:", optionFiles, 0, False)
                if ok and item2:
                    self._reinstaller.delete(item, item2)

    def _display_no_copy(self):
        entries = self._reinstaller._paths.getInstallerEntries()
        names = self._reinstaller._paths.getInstallerOptions()
        item, ok = QInputDialog.getItem(self.dialog, "Delete Installer", "Installer:", names, 0, False)

        if ok and item:
            item2, ok = QInputDialog.getItem(self.dialog, "Delete File", "File:", entries[item], 0, False)
            if ok and item2:
                self._reinstaller.delete(item, item2)
