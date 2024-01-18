try:
    from PyQt5.QtWidgets import QInputDialog, QLineEdit
    from PyQt5.QtCore import QCoreApplication
    from PyQt5 import QtWidgets
except:
    from PyQt6.QtWidgets import QInputDialog, QLineEdit
    from PyQt6.QtCore import QCoreApplication
    from PyQt6 import QtWidgets
from ..reinstaller_plugin import ReinstallerPlugin
import mobase, os

class ReinstallerInstallTool(ReinstallerPlugin, mobase.IPluginTool):
    
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
        return self.icons.checkIcon()
        
    def name(self):
        return self.baseName() + " Install Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Install"

    def description(self):
        return self.__tr("Runs an installer from a backed up file.")

    def display(self):
        item, ok = QInputDialog.getItem(self.dialog, "Run Installer", "Installer:", self.reinstaller.files.getInstallerOptions(), 0, False)
        if ok and item:
            files = self.reinstaller.files.getInstallerFileOptions(item) 
            if len(files) == 1:
                self.reinstaller.install(str(item), str(os.path.basename(str(files[0]))))
            if (len(files)) > 1:
                item2, ok = QInputDialog.getItem(self.dialog, "Select File", "File:", self.reinstaller.files.getFileNamesFromList(files), 0, False)
                if ok and item2:
                    self.reinstaller.install(str(item), str(item2))
