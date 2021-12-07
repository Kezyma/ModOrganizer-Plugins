from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtWidgets, QtCore
from pathlib import Path
from ..reinstaller_plugin import ReinstallerPlugin
import mobase


class ReinstallerManageTool(ReinstallerPlugin, mobase.IPluginTool):
    
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.dialog = self.getDialog()
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    #def displayName(self):
    #    return self.baseDisplayName()
    
    def description(self):
        return self.__tr("Opens Reinstaller manager.")

    def display(self):
        self.dialog.show()
        self.rebindUi()

    #def settings(self):
    #    return []

    #def name(self):
    #    return self.baseName()

    #def displayName(self):
    #    return self.baseDisplayName()
    
    #def icon(self):
    #    return self.icons.menuIcon()

    # Add File

    def addFileTextChanged(self):
        value = self.addFileText.text().strip()
        if value:
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

    def addFileSelectChanged(self):
        value = self.addFileSelect.currentText()
        if value:
            self.addFileText.setEnabled(True)
            self.addButton.setEnabled(True)
            self.addFileText.setText(str(value).split("-")[0].split(".")[0].strip())
        else:
            self.addFileText.setEnabled(False)
            self.addButton.setEnabled(False)

    def addButtonClick(self):
        name = self.reinstaller.create(self.addFileText.text().strip(), self.addFileSelect.currentText())
        self.rebindUi()
        return True

    # Install File

    def installerListChanged(self):
        item = self.installerList.currentItem()
        self.installerSelect.clear()
        self.installButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        if item:
            fileOptions = self.reinstaller.files.getFileNamesFromList(self.reinstaller.files.getInstallerFileOptions(item.text()))
            if len(fileOptions) > 0:
                self.installerSelect.addItems(fileOptions)
                self.installButton.setEnabled(True)
                self.deleteButton.setEnabled(True)

    def installButtonClick(self):
        modName = self.installerList.currentItem().text()
        modPath = self.installerSelect.currentText()
        self.reinstaller.install(str(modName), str(modPath))

    def deleteButtonClick(self):
        modName = self.installerList.currentItem().text()
        modPath = self.installerSelect.currentText()
        name = self.reinstaller.delete(str(modName), str(modPath))
        self.rebindUi()

    # UI Binding

    def rebindUi(self):
        self.addFileSelect.clear()
        self.addFileSelect.addItems(self.reinstaller.files.getDownloadFileOptions())

        self.installerList.clear()
        self.installerList.addItems(self.reinstaller.files.getInstallerOptions())

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        
        dialog.setObjectName("dialog")
        dialog.resize(560, 310)
        dialog.setWindowTitle("Reinstaller")

        ## Add New Mod
        self.addFileTextLabel = QtWidgets.QLabel(dialog)
        self.addFileTextLabel.setGeometry(QtCore.QRect(10, 5, 47, 13))
        self.addFileTextLabel.setObjectName("addFileTextLabel")
        self.addFileTextLabel.setText("Name")

        self.addFileText = QtWidgets.QLineEdit(dialog)
        self.addFileText.setGeometry(QtCore.QRect(10, 20, 180, 20))
        self.addFileText.setObjectName("addFileText")
        self.addFileText.setEnabled(False)
        self.addFileText.textChanged.connect(self.addFileTextChanged)

        self.addFileSelectLabel = QtWidgets.QLabel(dialog)
        self.addFileSelectLabel.setGeometry(QtCore.QRect(200, 5, 47, 13))
        self.addFileSelectLabel.setObjectName("addFileSelectLabel")
        self.addFileSelectLabel.setText("File")

        self.addFileSelect = QtWidgets.QComboBox(dialog)
        self.addFileSelect.setGeometry(QtCore.QRect(200, 20, 280, 20))
        self.addFileSelect.setObjectName("addFileSelect")
        self.addFileSelect.currentIndexChanged.connect(self.addFileSelectChanged)

        self.addButton = QtWidgets.QPushButton(dialog)
        self.addButton.setGeometry(QtCore.QRect(490, 19, 60, 22))
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.addButton.setEnabled(False)
        self.addButton.clicked.connect(self.addButtonClick)

        self.line = QtWidgets.QFrame(dialog)
        self.line.setGeometry(QtCore.QRect(0, 45, 560, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Select Existing Mod
        self.installersLabel = QtWidgets.QLabel(dialog)
        self.installersLabel.setGeometry(QtCore.QRect(10, 60, 47, 13))
        self.installersLabel.setObjectName("installersLabel")
        self.installersLabel.setText("Installers")

        self.installerList = QtWidgets.QListWidget(dialog)
        self.installerList.setGeometry(QtCore.QRect(10, 75, 540, 200))
        self.installerList.setObjectName("installerList")
        self.installerList.currentItemChanged.connect(self.installerListChanged)
        
        self.installerSelect = QtWidgets.QComboBox(dialog)
        self.installerSelect.setGeometry(QtCore.QRect(10, 280, 400, 21))
        self.installerSelect.setObjectName("installerSelect")

        self.installButton = QtWidgets.QPushButton(dialog)
        self.installButton.setGeometry(QtCore.QRect(420, 279, 60, 22))
        self.installButton.setObjectName("installButton")
        self.installButton.setText("Install")
        self.installButton.setEnabled(False)
        self.installButton.clicked.connect(self.installButtonClick)

        self.deleteButton = QtWidgets.QPushButton(dialog)
        self.deleteButton.setGeometry(QtCore.QRect(490, 279, 60, 22))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Delete")
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteButtonClick)

        QtCore.QMetaObject.connectSlotsByName(dialog)

        return  dialog

    
