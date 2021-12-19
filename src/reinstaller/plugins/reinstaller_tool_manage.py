try:
    from PyQt5.QtWidgets import QInputDialog, QLineEdit
    from PyQt5.QtCore import QCoreApplication
    from PyQt5 import QtWidgets, QtCore
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
except:
    from PyQt6.QtWidgets import QInputDialog, QLineEdit
    from PyQt6.QtCore import QCoreApplication
    from PyQt6 import QtWidgets, QtCore
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
from pathlib import Path
from ..reinstaller_plugin import ReinstallerPlugin
import mobase


class ReinstallerManageTool(ReinstallerPlugin, mobase.IPluginTool):
    
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)
    
    def description(self):
        return self.__tr("Opens Reinstaller manager.")

    def display(self):
        self.dialog.show()
        self.rebindUi()
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
            self.addFileText.setText(self.reinstaller.files.getDownloadFileName(value))
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
        dialog.resize(420, 230)
        dialog.setWindowIcon(self.icon())
        dialog.setWindowFlags(qtStaysOnTop)
        dialog.setWindowTitle("Reinstaller")
        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setContentsMargins(5, 5, 5, 5)
        self.dialogLayout.setSpacing(5)
        self.dialogLayout.setObjectName("dialogLayout")

        ## Add New Mod
        self.addWidget = QtWidgets.QWidget(dialog)
        self.addWidget.setObjectName("addWidget")
        self.addLayout = QtWidgets.QHBoxLayout(self.addWidget)
        self.addLayout.setContentsMargins(0, 0, 0, 0)
        self.addLayout.setSpacing(5)
        self.addLayout.setObjectName("addLayout")

        self.addFileText = QtWidgets.QLineEdit(self.addWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFileText.sizePolicy().hasHeightForWidth())
        self.addFileText.setSizePolicy(sizePolicy)
        self.addFileText.setObjectName("addFileText")
        self.addLayout.addWidget(self.addFileText, 1)
        self.addFileText.setEnabled(False)
        self.addFileText.textChanged.connect(self.addFileTextChanged)

        self.addFileSelect = QtWidgets.QComboBox(self.addWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addFileSelect.sizePolicy().hasHeightForWidth())
        self.addFileSelect.setSizePolicy(sizePolicy)
        self.addFileSelect.setObjectName("addFileSelect")
        self.addFileSelect.currentIndexChanged.connect(self.addFileSelectChanged)
        self.addLayout.addWidget(self.addFileSelect, 1)

        self.addButton = QtWidgets.QPushButton(self.addWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setIcon(self.icons.plusIcon())
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.addButton.setEnabled(False)
        self.addButton.clicked.connect(self.addButtonClick)
        self.addLayout.addWidget(self.addButton)

        self.dialogLayout.addWidget(self.addWidget)

        # Select Existing Mod
        self.installerList = QtWidgets.QListWidget(dialog)
        self.installerList.setObjectName("installerList")
        self.dialogLayout.addWidget(self.installerList)
        self.installerList.currentItemChanged.connect(self.installerListChanged)

        self.installWidget = QtWidgets.QWidget(dialog)
        self.installWidget.setObjectName("installWidget")
        self.installLayout = QtWidgets.QHBoxLayout(self.installWidget)
        self.installLayout.setContentsMargins(0, 0, 0, 0)
        self.installLayout.setSpacing(5)
        self.installLayout.setObjectName("installLayout")
        
        self.installerSelect = QtWidgets.QComboBox(self.installWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installerSelect.sizePolicy().hasHeightForWidth())
        self.installerSelect.setSizePolicy(sizePolicy)
        self.installerSelect.setObjectName("installerSelect")
        self.installLayout.addWidget(self.installerSelect)

        self.installButton = QtWidgets.QPushButton(self.installWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installButton.sizePolicy().hasHeightForWidth())
        self.installButton.setSizePolicy(sizePolicy)
        self.installButton.setIcon(self.icons.downloadIcon())
        self.installButton.setObjectName("installButton")
        self.installLayout.addWidget(self.installButton)
        self.installButton.setText("Install")
        self.installButton.setEnabled(False)
        self.installButton.clicked.connect(self.installButtonClick)

        self.deleteButton = QtWidgets.QPushButton(self.installWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        self.deleteButton.setIcon(self.icons.trashIcon())
        self.deleteButton.setObjectName("deleteButton")
        self.installLayout.addWidget(self.deleteButton)
        self.deleteButton.setText("Delete")
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteButtonClick)

        self.dialogLayout.addWidget(self.installWidget)

        QtCore.QMetaObject.connectSlotsByName(dialog)
        return dialog

    
