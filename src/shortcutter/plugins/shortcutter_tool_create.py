from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
from PyQt5.QtCore import QCoreApplication, qInfo, QSize
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileIconProvider
from ..shortcutter_plugin import ShortcutterPlugin
import mobase

class ShortcutterCreateTool(ShortcutterPlugin, mobase.IPluginTool):
    
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.dialog = self.getDialog()
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.linkIcon()
        
    def description(self):
        return self.__tr("Creates a shortcut.")

    def display(self):
        self.dialog.show()
        self.rebindUi()
        self.setInitialSettings()

    def createShortcut(self):
        profile = self.profileSelect.currentText()
        app = self.appSelect.currentText()
        label = self.nameText.text()
        icon = self.selectedIcon.text()
        self.shortcutter.create(label, profile, app, self.shortcutter.paths.currentInstanceName(), icon)

    def rebindUi(self):
        self.appSelect.clear()
        self.appSelect.addItems(self.shortcutter.paths.modOrganizerApps())
        self.profileSelect.clear()
        self.profileSelect.addItems(self.shortcutter.files.getFileNamesFromList(self.shortcutter.files.getSubFolderList(self.shortcutter.paths.modOrganizerProfilesPath(), False)))
        
    def setInitialSettings(self):
        self.profileSelect.setCurrentText(self.shortcutter.paths.modOrganizerProfile())
        self.selectChange()

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        self.setupUi(dialog)
        return dialog

    def selectChange(self):
        self.nameText.setText(self.profileSelect.currentText() + " - " + self.appSelect.currentText())
        appPaths = self.shortcutter.paths.modOrganizerAppPaths()
        if self.appSelect.currentText() in appPaths:
            iconPath = str(appPaths[self.appSelect.currentText()])
            self.selectedIcon.setText(iconPath)
            self.updateIconDisplay()

    def selectIcon(self):
        fileDialog = QFileDialog(self.dialog)
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setNameFilter("Icons (*.ico *.exe)")
        files = []
        if fileDialog.exec():
            files = fileDialog.selectedFiles()
            if len(files) > 0:
                self.selectedIcon.setText(files[0])
                self.updateIconDisplay()

    def updateIconDisplay(self):
        iconFile = QtCore.QFileInfo(self.selectedIcon.text())
        ip = QFileIconProvider()
        icon = ip.icon(iconFile)
        pix = icon.pixmap(QSize(23, 23))
        self.shortcutIcon.setPixmap(pix)
    
    def setupUi(self, widget):
        widget.setObjectName("Shortcutter")
        widget.resize(400, 215)
        widget.setFixedSize(400, 215)

        self.buttonBox = QtWidgets.QDialogButtonBox(widget)
        self.buttonBox.setGeometry(QtCore.QRect(230, 180, 166, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.profileLabel = QtWidgets.QLabel(widget)
        self.profileLabel.setGeometry(QtCore.QRect(5, 50, 391, 16))
        self.profileLabel.setObjectName("profileLabel")
        self.profileSelect = QtWidgets.QComboBox(widget)
        self.profileSelect.setGeometry(QtCore.QRect(5, 65, 391, 22))
        self.profileSelect.setObjectName("profileSelect")
        self.profileSelect.currentTextChanged.connect(self.selectChange)

        self.applicationLabel = QtWidgets.QLabel(widget)
        self.applicationLabel.setGeometry(QtCore.QRect(5, 95, 391, 16))
        self.applicationLabel.setObjectName("applicationLabel")
        self.appSelect = QtWidgets.QComboBox(widget)
        self.appSelect.setGeometry(QtCore.QRect(5, 110, 391, 22))
        self.appSelect.setObjectName("appSelect")
        self.appSelect.currentTextChanged.connect(self.selectChange)

        self.iconLabel = QtWidgets.QLabel(widget)
        self.iconLabel.setGeometry(QtCore.QRect(5, 140, 391, 16))
        self.iconLabel.setObjectName("iconLabel")
        self.iconButton = QtWidgets.QPushButton(widget)
        self.iconButton.setGeometry(QtCore.QRect(33, 155, 75, 23))
        self.iconButton.setObjectName("iconButton")
        self.iconButton.clicked.connect(self.selectIcon)

        self.selectedIcon = QtWidgets.QLabel(widget)
        self.selectedIcon.setGeometry(QtCore.QRect(113, 160, 391, 13))
        self.selectedIcon.setObjectName("selectedIcon")

        self.nameLabel = QtWidgets.QLabel(widget)
        self.nameLabel.setGeometry(QtCore.QRect(5, 5, 391, 16))
        self.nameLabel.setObjectName("nameLabel")
        self.nameText = QtWidgets.QLineEdit(widget)
        self.nameText.setGeometry(QtCore.QRect(5, 20, 391, 21))
        self.nameText.setObjectName("nameText")

        self.shortcutIcon = QtWidgets.QLabel(widget)
        self.shortcutIcon.setGeometry(QtCore.QRect(5, 155, 23, 23))
        self.shortcutIcon.setObjectName("shortcutIcon")
        self.shortcutIcon.setScaledContents(True)

        widget.setWindowTitle("Shortcutter")
        self.profileLabel.setText("Profile")
        self.applicationLabel.setText("Application")
        self.iconLabel.setText("Icon")
        self.iconButton.setText("Select")
        self.selectedIcon.setText("...")
        self.nameLabel.setText("Name")

        #self.buttonBox.accepted.connect(widget.accept)
        self.buttonBox.accepted.connect(self.createShortcut)
        self.buttonBox.rejected.connect(widget.reject)
        QtCore.QMetaObject.connectSlotsByName(widget)