from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets
from ..reinstaller_plugin import ReinstallerPlugin
import mobase, shutil, os

class ReinstallerDeleteTool(ReinstallerPlugin, mobase.IPluginTool):
    
    def __init__(self):
        self.dialog = QtWidgets.QWidget()
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []

    def icon(self):
        return self.icons.minusIcon()
        
    def name(self):
        return self.baseName() + " Delete Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Delete"

    def description(self):
        return self.__tr("Deletes a downloaded file.")

    def display(self):
        installers = self.reinstaller.files.getSubFolderList(self.reinstaller.paths.pluginDataPath())
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))

        item, ok = QInputDialog.getItem(self.dialog, "Delete Installer", "Installer:", names, 0, False)
        if ok and item:
            installerOpts = self.reinstaller.files.getFolderFileList(self.reinstaller.paths.pluginDataPath() / item)
            files = []
            for file in installerOpts:
                if not str(file).endswith('.meta'):
                    files.append(file)
            if len(files) == 1:
                self.reinstaller.delete(item, os.path.basename(files[0]))
            if (len(files)) > 1:
                optionFiles = []
                for opt in files:
                    optionFiles.append(os.path.basename(opt))
                item2, ok = QInputDialog.getItem(self.dialog, "Delete File", "File:", optionFiles, 0, False)
                if ok and item2:
                    self.reinstaller.delete(item, item2)



