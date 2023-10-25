try:
    from PyQt5.QtWidgets import QInputDialog, QLineEdit
    from PyQt5.QtCore import QCoreApplication
    from PyQt5 import QtWidgets
except:
    from PyQt6.QtWidgets import QInputDialog, QLineEdit
    from PyQt6.QtCore import QCoreApplication
    from PyQt6 import QtWidgets
from ..reinstaller_plugin import ReinstallerPlugin
import mobase

class ReinstallerCreateTool(ReinstallerPlugin, mobase.IPluginTool):
    
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
        return self.icons.plusIcon()
        
    def name(self):
        return self.baseName() + " Create Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Create"

    def description(self):
        return self.__tr("Creates a new installer from a downloaded file.")

    def display(self):
        modFiles = self.reinstaller.files.getDownloadFileOptions()
        item, ok = QInputDialog.getItem(self.dialog, "Select Installer", "Installer:", modFiles, 0, False)
        if ok and item:
            name, ok = QInputDialog.getText(self.dialog, "Name", "Installer Name:", QLineEdit.Normal, self.reinstaller.files.getDownloadFileName(str(item)))
            if ok and name:
                self.reinstaller.create(str(name), str(item))
