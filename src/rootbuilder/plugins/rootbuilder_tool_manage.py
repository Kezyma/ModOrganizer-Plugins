from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore, QtWidgets
from ..rootbuilder_plugin import RootBuilderPlugin
import mobase

class RootBuilderManageTool(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.dialog = self.getDialog()
        return super().init(organiser)

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        
        # Panel Settings
        dialog.setObjectName("dialog")
        dialog.resize(431, 406)
        dialog.setWindowTitle("Root Builder")

        # Build, Sync & Clear Settings
        self.buildButton = QtWidgets.QPushButton(dialog)
        self.buildButton.setGeometry(QtCore.QRect(5, 5, 141, 23))
        self.buildButton.setObjectName("buildButton")
        self.buildButton.setText("Build")
        self.buildButton.clicked.connect(self.buildClick)

        self.syncButton = QtWidgets.QPushButton(dialog)
        self.syncButton.setGeometry(QtCore.QRect(145, 5, 141, 23))
        self.syncButton.setObjectName("syncButton")
        self.syncButton.setText("Sync")
        self.syncButton.clicked.connect(self.syncClick)

        self.clearButton = QtWidgets.QPushButton(dialog)
        self.clearButton.setGeometry(QtCore.QRect(285, 5, 141, 23))
        self.clearButton.setObjectName("clearButton")
        self.clearButton.setText("Clear")
        self.clearButton.clicked.connect(self.clearClick)
        
        self.line = QtWidgets.QFrame(dialog)
        self.line.setGeometry(QtCore.QRect(0, 30, 431, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Backup Settings
        self.backupButton = QtWidgets.QPushButton(dialog)
        self.backupButton.setGeometry(QtCore.QRect(5, 45, 211, 23))
        self.backupButton.setObjectName("backupButton")
        self.backupButton.setText("Create Backup")
        self.backupButton.clicked.connect(self.backupClick)

        self.delBackupButton = QtWidgets.QPushButton(dialog)
        self.delBackupButton.setGeometry(QtCore.QRect(5, 70, 211, 23))
        self.delBackupButton.setObjectName("delBackupButton")
        self.delBackupButton.setText("Delete Backup")
        self.delBackupButton.clicked.connect(self.delBackupClick)

        # Cache Settings
        self.cacheButton = QtWidgets.QPushButton(dialog)
        self.cacheButton.setGeometry(QtCore.QRect(215, 45, 211, 23))
        self.cacheButton.setObjectName("cacheButton")
        self.cacheButton.setText("Create Cache")
        self.cacheButton.clicked.connect(self.cacheClick)
        
        self.delCacheButton = QtWidgets.QPushButton(dialog)
        self.delCacheButton.setGeometry(QtCore.QRect(215, 70, 211, 23))
        self.delCacheButton.setObjectName("delCacheButton")
        self.delCacheButton.setText("Delete Cache")
        self.delCacheButton.clicked.connect(self.delCacheClick)

        self.line_2 = QtWidgets.QFrame(dialog)
        self.line_2.setGeometry(QtCore.QRect(0, 95, 431, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # Mode Settings
        self.methodLabel = QtWidgets.QLabel(dialog)
        self.methodLabel.setGeometry(QtCore.QRect(10, 110, 47, 13))
        self.methodLabel.setObjectName("methodLabel")
        self.methodLabel.setText("Method")

        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(120, 110, 301, 106))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setText("<html><head/><body><p>Copy - <span style=\" font-style:italic;\">Build copies files to the game folder.</span></p><p>USVFS - <span style=\" font-style:italic;\">(Autobuild only) uses Mod Organizer\'s file system to add files to the game folder.</span></p><p>USVFS + Links - <span style=\" font-style:italic;\">(Autobuild only) uses Mod Organizer\'s file system to add files to the game folder. Adds links for specific files to increase compatibility.</span></p></body></html>")

        self.copyButton = QtWidgets.QRadioButton(dialog)
        self.copyButton.setGeometry(QtCore.QRect(10, 125, 100, 17))
        self.copyButton.setObjectName("copyButton")
        self.copyButton.setText("Copy")
        self.copyButton.clicked.connect(self.copyModeChanged)

        self.usvfsButton = QtWidgets.QRadioButton(dialog)
        self.usvfsButton.setGeometry(QtCore.QRect(10, 145, 100, 17))
        self.usvfsButton.setObjectName("usvfsButton")
        self.usvfsButton.setText("USVFS")
        self.usvfsButton.clicked.connect(self.usvfsModeChanged)

        self.linkButton = QtWidgets.QRadioButton(dialog)
        self.linkButton.setGeometry(QtCore.QRect(10, 165, 100, 17))
        self.linkButton.setObjectName("linkButton")
        self.linkButton.setText("USVFS + Links")
        self.linkButton.clicked.connect(self.linkModeChanged)

        self.line_3 = QtWidgets.QFrame(dialog)
        self.line_3.setGeometry(QtCore.QRect(0, 215, 431, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # Misc Settings
        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 270, 331, 16))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("<html><head/><body><p><span style=\" font-style:italic;\">- Automatic build &amp; clear when running apps through Mod Organizer.</span></p></body></html>")
        self.autobuildCheck = QtWidgets.QCheckBox(dialog)
        self.autobuildCheck.setGeometry(QtCore.QRect(10, 270, 71, 17))
        self.autobuildCheck.setObjectName("autobuildCheck")
        self.autobuildCheck.setText("Autobuild")
        self.autobuildCheck.clicked.connect(self.autobuildChanged)

        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(80, 290, 331, 16))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")        
        self.label_3.setText("<html><head/><body><p><span style=\" font-style:italic;\">- Redirect apps being run from Root folders to the game folder.</span></p></body></html>")
        self.redirectCheck = QtWidgets.QCheckBox(dialog)
        self.redirectCheck.setGeometry(QtCore.QRect(10, 290, 70, 17))
        self.redirectCheck.setObjectName("redirectCheck")
        self.redirectCheck.setText("Redirect")
        self.redirectCheck.clicked.connect(self.redirectChanged)

        self.backupLabel = QtWidgets.QLabel(dialog)
        self.backupLabel.setGeometry(QtCore.QRect(80, 250, 331, 16))
        self.backupLabel.setWordWrap(True)
        self.backupLabel.setObjectName("backupLabel")
        self.backupLabel.setText("<html><head/><body><p><span style=\" font-style:italic;\">- Backs up game files to ensure successful restore.</span></p></body></html>")
        self.backupCheck = QtWidgets.QCheckBox(dialog)
        self.backupCheck.setGeometry(QtCore.QRect(10, 250, 70, 17))
        self.backupCheck.setObjectName("backupCheck")
        self.backupCheck.setText("Backup")
        self.backupCheck.clicked.connect(self.backupChanged)

        self.cacheLabel = QtWidgets.QLabel(dialog)
        self.cacheLabel.setGeometry(QtCore.QRect(80, 230, 331, 16))
        self.cacheLabel.setWordWrap(True)
        self.cacheLabel.setObjectName("cacheLabel")
        self.cacheLabel.setText("<html><head/><body><p><span style=\" font-style:italic;\">- Caches file hashes on first run, reused for all future runs.</span></p></body></html>")
        self.cacheCheck = QtWidgets.QCheckBox(dialog)
        self.cacheCheck.setGeometry(QtCore.QRect(10, 230, 71, 17))
        self.cacheCheck.setObjectName("cacheCheck")
        self.cacheCheck.setText("Cache")
        self.cacheCheck.clicked.connect(self.cacheChanged)

        self.linksLabel = QtWidgets.QLabel(dialog)
        self.linksLabel.setGeometry(QtCore.QRect(10, 310, 411, 16))
        self.linksLabel.setObjectName("linksLabel")
        self.linksLabel.setText("<html><head/><body><p>Link Extensions - <span style=\" font-style:italic;\">Extensions to create links for using USVFS + Link mode.</span></p></body></html>")
        self.linkText = QtWidgets.QLineEdit(dialog)
        self.linkText.setGeometry(QtCore.QRect(10, 330, 411, 20))
        self.linkText.setObjectName("linkText")
        self.linkText.textChanged.connect(self.linkExtensionsChanged)

        self.exclusionsLabel = QtWidgets.QLabel(dialog)
        self.exclusionsLabel.setGeometry(QtCore.QRect(10, 355, 411, 16))
        self.exclusionsLabel.setObjectName("exclusionsLabel")
        self.exclusionsLabel.setText("<html><head/><body><p>Exclusions - <span style=\" font-style:italic;\">Files and folders to exclude from backup and cache.</span></p></body></html>")
        self.exclusionsText = QtWidgets.QLineEdit(dialog)
        self.exclusionsText.setGeometry(QtCore.QRect(10, 375, 411, 20))
        self.exclusionsText.setObjectName("exclusionsText")
        self.exclusionsText.textChanged.connect(self.exclusionsTextChanged)
        
        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []

    def icon(self):
        return self.icons.menuIcon()

    def name(self):
        return self.baseName() + " Manager Tool"

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Root Builder Manager.")
    
    def display(self):
        self.dialog.show()
        self.bindSettings()

    def bindSettings(self):
        copyMode = not self.rootBuilder.settings.usvfsmode()
        usvfsMode = not copyMode
        linkMode = usvfsMode and self.rootBuilder.settings.linkmode()
        self.copyButton.setChecked(copyMode)
        self.copyModeChanged()
        self.usvfsButton.setChecked(usvfsMode)
        self.usvfsModeChanged()
        self.linkButton.setChecked(linkMode)
        self.linkModeChanged()

        self.autobuildCheck.setChecked(self.rootBuilder.settings.autobuild())
        self.redirectCheck.setChecked(self.rootBuilder.settings.redirect())
        self.backupCheck.setChecked(self.rootBuilder.settings.backup())
        self.cacheCheck.setChecked(self.rootBuilder.settings.cache())

        self.linkText.setText(self.organiser.pluginSetting("RootBuilder", "linkextensions"))
        self.exclusionsText.setText(self.organiser.pluginSetting("RootBuilder", "exclusions"))    
            
    def bindActions(self):
        if not self.rootBuilder.settings.usvfsmode():
            self.buildButton.setEnabled(True)
            if self.rootBuilder.copier.hasModData():
                self.syncButton.setEnabled(True)
                self.clearButton.setEnabled(True)
            else:
                self.syncButton.setEnabled(False)
                self.clearButton.setEnabled(False)
        else:
            self.buildButton.setEnabled(False)
            self.syncButton.setEnabled(False)
            self.clearButton.setEnabled(False)

        if self.rootBuilder.copier.hasModData() or self.rootBuilder.paths.rootLinkDataFilePath().exists():
            self.backupButton.setEnabled(False)
            self.delBackupButton.setEnabled(False)
            self.cacheButton.setEnabled(False)
            self.delCacheButton.setEnabled(False)
        else:
            self.backupButton.setEnabled(True)
            self.delBackupButton.setEnabled(True)
            self.cacheButton.setEnabled(True)
            self.delCacheButton.setEnabled(True)

    def buildClick(self):
        self.rootBuilder.build()
        self.syncButton.setEnabled(True)
        self.clearButton.setEnabled(True)
        self.bindActions()

    def syncClick(self):
        self.rootBuilder.sync()

    def clearClick(self):
        self.rootBuilder.clear()
        self.clearButton.setEnabled(False)
        self.syncButton.setEnabled(False)
        self.bindActions()

    def backupClick(self):
        self.rootBuilder.backup.backup()
        self.rootBuilder.backup.clearFileData()

    def cacheClick(self):
        self.rootBuilder.backup.buildCache()
    
    def delBackupClick(self):
        self.rootBuilder.backup.clearBackupFiles()
        self.rootBuilder.backup.clearFileData()

    def delCacheClick(self):
        self.rootBuilder.backup.clearCache()

    def cacheChanged(self):
        self.updateSetting("cache", self.cacheCheck.isChecked())
    
    def backupChanged(self):
        self.updateSetting("backup", self.backupCheck.isChecked())

    def autobuildChanged(self):
        self.updateSetting("autobuild", self.autobuildCheck.isChecked())

    def redirectChanged(self):
        self.updateSetting("redirect", self.redirectCheck.isChecked())

    def copyModeChanged(self):
        if self.copyButton.isChecked():
            self.updateSetting("usvfsmode", False)
            self.updateSetting("linkmode", False)
            self.autobuildCheck.setEnabled(True)
            self.linkText.setEnabled(False)
            self.bindActions()

    def usvfsModeChanged(self):
        if self.usvfsButton.isChecked():
            self.updateSetting("usvfsmode", True)
            self.updateSetting("linkmode", False)
            self.updateSetting("autobuild", True)
            self.autobuildCheck.setChecked(True)
            self.autobuildCheck.setEnabled(False)
            self.linkText.setEnabled(False)
            self.bindActions()

    def linkModeChanged(self):
        if self.linkButton.isChecked():
            self.updateSetting("usvfsmode", True)
            self.updateSetting("linkmode", True)
            self.updateSetting("autobuild", True)
            self.autobuildCheck.setChecked(True)
            self.autobuildCheck.setEnabled(False)
            self.linkText.setEnabled(True)
            self.bindActions()

    def exclusionsTextChanged(self):
        self.updateSetting("exclusions", self.exclusionsText.text())

    def linkExtensionsChanged(self):
        self.updateSetting("linkextensions", self.linkText.text())

    def updateSetting(self, name, value):
        self.organiser.setPluginSetting("RootBuilder", name, value)
        