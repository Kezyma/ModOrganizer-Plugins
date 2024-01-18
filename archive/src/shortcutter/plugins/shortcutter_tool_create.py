try:
    from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
    from PyQt5.QtCore import QCoreApplication, qInfo, QSize
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtWidgets import QFileIconProvider
    qtHorizontal = QtCore.Qt.Horizontal
    qtCancel = QtWidgets.QDialogButtonBox.Cancel
    qtOkay = QtWidgets.QDialogButtonBox.Ok
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
    from PyQt6.QtCore import QCoreApplication, qInfo, QSize
    from PyQt6 import QtGui, QtWidgets, QtCore
    from PyQt6.QtWidgets import QFileIconProvider
    qtHorizontal = QtCore.Qt.Orientation.Horizontal
    qtCancel = QtWidgets.QDialogButtonBox.StandardButton.Cancel
    qtOkay = QtWidgets.QDialogButtonBox.StandardButton.Ok
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy.Policy
from ..shortcutter_plugin import ShortcutterPlugin
import mobase

class ShortcutterCreateTool(ShortcutterPlugin, mobase.IPluginTool):
    
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        return res

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
        
    invalidCharacters = '|<>"?*:/\\'
    def createShortcut(self):
        profile = self.profileSelect.currentText()
        app = self.appSelect.currentText()
        label = str(self.nameText.text())
        for character in self.invalidCharacters:
            label = str(label).replace(character, "")
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
    
    def getDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setObjectName("dialog")
        dialog.resize(400, 136)
        dialog.setMinimumWidth(200)
        dialog.setWindowIcon(self.icon())
        #dialog.setWindowFlags(qtStaysOnTop)
        dialog.setWindowTitle("Shortcutter")
        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setContentsMargins(5, 5, 5, 5)
        self.dialogLayout.setSpacing(5)
        self.dialogLayout.setObjectName("dialogLayout")
        
        self.nameWidget = QtWidgets.QWidget(dialog)
        self.nameWidget.setObjectName("nameWidget")
        self.nameLayout = QtWidgets.QHBoxLayout(self.nameWidget)
        self.nameLayout.setContentsMargins(0, 0, 0, 0)
        self.nameLayout.setSpacing(5)
        self.nameLayout.setObjectName("nameLayout")
        self.nameLabel = QtWidgets.QLabel(self.nameWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        self.nameLabel.setMinimumSize(QtCore.QSize(65, 0))
        self.nameLabel.setObjectName("nameLabel")
        self.nameLabel.setText("Name")
        self.nameLayout.addWidget(self.nameLabel)
        self.nameText = QtWidgets.QLineEdit(self.nameWidget)
        self.nameText.setObjectName("nameText")
        self.nameLayout.addWidget(self.nameText)
        self.dialogLayout.addWidget(self.nameWidget)

        self.profileWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileWidget.sizePolicy().hasHeightForWidth())
        self.profileWidget.setSizePolicy(sizePolicy)
        self.profileWidget.setObjectName("profileWidget")
        self.profileLayout = QtWidgets.QHBoxLayout(self.profileWidget)
        self.profileLayout.setContentsMargins(0, 0, 0, 0)
        self.profileLayout.setSpacing(5)
        self.profileLayout.setObjectName("profileLayout")
        self.profileLabel = QtWidgets.QLabel(self.profileWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileLabel.sizePolicy().hasHeightForWidth())
        self.profileLabel.setSizePolicy(sizePolicy)
        self.profileLabel.setMinimumSize(QtCore.QSize(65, 0))
        self.profileLabel.setObjectName("profileLabel")
        self.profileLabel.setText("Profile")
        self.profileLayout.addWidget(self.profileLabel)
        self.profileSelect = QtWidgets.QComboBox(self.profileWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileSelect.sizePolicy().hasHeightForWidth())
        self.profileSelect.setSizePolicy(sizePolicy)
        self.profileSelect.setObjectName("profileSelect")
        self.profileSelect.currentTextChanged.connect(self.selectChange)
        self.profileLayout.addWidget(self.profileSelect)
        self.dialogLayout.addWidget(self.profileWidget)

        self.appWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appWidget.sizePolicy().hasHeightForWidth())
        self.appWidget.setSizePolicy(sizePolicy)
        self.appWidget.setObjectName("appWidget")
        self.appLayout = QtWidgets.QHBoxLayout(self.appWidget)
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.appLayout.setSpacing(5)
        self.appLayout.setObjectName("appLayout")
        self.appLabel = QtWidgets.QLabel(self.appWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appLabel.sizePolicy().hasHeightForWidth())
        self.appLabel.setSizePolicy(sizePolicy)
        self.appLabel.setMinimumSize(QtCore.QSize(65, 0))
        self.appLabel.setObjectName("appLabel")
        self.appLabel.setText("Application")
        self.appLayout.addWidget(self.appLabel)
        self.appSelect = QtWidgets.QComboBox(self.appWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appSelect.sizePolicy().hasHeightForWidth())
        self.appSelect.setSizePolicy(sizePolicy)
        self.appSelect.setObjectName("appSelect")
        self.appSelect.currentTextChanged.connect(self.selectChange)
        self.appLayout.addWidget(self.appSelect)
        self.dialogLayout.addWidget(self.appWidget)

        self.iconWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconWidget.sizePolicy().hasHeightForWidth())
        self.iconWidget.setSizePolicy(sizePolicy)
        self.iconWidget.setObjectName("iconWidget")
        self.iconLayout = QtWidgets.QHBoxLayout(self.iconWidget)
        self.iconLayout.setContentsMargins(0, 0, 0, 0)
        self.iconLayout.setSpacing(5)
        self.iconLayout.setObjectName("iconLayout")
        self.iconLabel = QtWidgets.QLabel(self.iconWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(65, 0))
        self.iconLabel.setObjectName("iconLabel")
        self.iconLabel.setText("Icon")
        self.iconLayout.addWidget(self.iconLabel)
        self.shortcutIcon = QtWidgets.QLabel(self.iconWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shortcutIcon.sizePolicy().hasHeightForWidth())
        self.shortcutIcon.setSizePolicy(sizePolicy)
        self.shortcutIcon.setMinimumSize(QtCore.QSize(23, 23))
        self.shortcutIcon.setMaximumSize(QtCore.QSize(23, 23))
        self.shortcutIcon.setText("")
        self.shortcutIcon.setObjectName("shortcutIcon")
        self.shortcutIcon.setScaledContents(True)
        self.iconLayout.addWidget(self.shortcutIcon)
        self.iconButton = QtWidgets.QPushButton(self.iconWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconButton.sizePolicy().hasHeightForWidth())
        self.iconButton.setSizePolicy(sizePolicy)
        self.iconButton.setObjectName("iconButton")
        self.iconButton.setText("Select")
        self.iconButton.clicked.connect(self.selectIcon)
        self.iconLayout.addWidget(self.iconButton)
        self.selectedIcon = QtWidgets.QLabel(self.iconWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedIcon.sizePolicy().hasHeightForWidth())
        self.selectedIcon.setSizePolicy(sizePolicy)
        self.selectedIcon.setObjectName("iconPathLabel")
        self.selectedIcon.setText("...")
        self.iconLayout.addWidget(self.selectedIcon)
        self.dialogLayout.addWidget(self.iconWidget)

        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(qtHorizontal)
        self.buttonBox.setStandardButtons(qtCancel|qtOkay)
        self.buttonBox.setObjectName("buttonBox")
        self.dialogLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.createShortcut)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog

        
        
        
        
        
        
        