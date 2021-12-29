try:
    from PyQt5.QtCore import QCoreApplication, qInfo
    from PyQt5 import QtCore, QtWidgets
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
    from PyQt6 import QtCore, QtWidgets
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy.Policy
from ..rootbuilder_plugin import RootBuilderPlugin
import mobase

class RootBuilderManageTool(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        return res

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        
        # Panel Settings
        dialog.setObjectName("dialog")
        dialog.resize(465, 400)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setMinimumSize(QtCore.QSize(465, 400))
        dialog.setWindowTitle("Root Builder")
        dialog.setWindowIcon(self.icon())
        #dialog.setWindowFlags(qtStaysOnTop)
        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setContentsMargins(5, 5, 5, 5)
        self.dialogLayout.setSpacing(5)
        self.dialogLayout.setObjectName("dialogLayout")

        # Mode Settings
        self.modeContainer = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.modeContainer.sizePolicy().hasHeightForWidth())
        self.modeContainer.setSizePolicy(sizePolicy)
        self.modeContainer.setObjectName("modeContainer")
        self.modeLayout = QtWidgets.QVBoxLayout(self.modeContainer)
        self.modeLayout.setContentsMargins(0, 0, 0, 0)
        self.modeLayout.setSpacing(0)
        self.modeLayout.setObjectName("modeLayout")

        self.modeLabel = QtWidgets.QLabel(self.modeContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modeLabel.sizePolicy().hasHeightForWidth())
        self.modeLabel.setSizePolicy(sizePolicy)
        self.modeLabel.setObjectName("modeLabel")        
        self.modeLabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Mode</span></p></body></html>")
        self.modeLayout.addWidget(self.modeLabel)

        # Copy
        self.copyContainer = QtWidgets.QWidget(self.modeContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyContainer.sizePolicy().hasHeightForWidth())
        self.copyContainer.setSizePolicy(sizePolicy)
        self.copyContainer.setObjectName("copyContainer")
        self.copyLayout = QtWidgets.QHBoxLayout(self.copyContainer)
        self.copyLayout.setContentsMargins(0, 0, 0, 0)
        self.copyLayout.setSpacing(5)
        self.copyLayout.setObjectName("copyLayout")
        self.copyButton = QtWidgets.QRadioButton(self.copyContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyButton.sizePolicy().hasHeightForWidth())
        self.copyButton.setSizePolicy(sizePolicy)
        self.copyButton.setMinimumSize(QtCore.QSize(100, 0))
        self.copyButton.setObjectName("copyButton")
        self.copyButton.setText("Copy")
        self.copyButton.clicked.connect(self.copyModeChanged)
        self.copyLayout.addWidget(self.copyButton)
        self.copyLabel = QtWidgets.QLabel(self.copyContainer)
        self.copyLabel.setWordWrap(True)
        self.copyLabel.setObjectName("copyLabel")
        self.copyLabel.setText("Building copies files from root mods to the game folder. Highest compatibility.")
        self.copyLayout.addWidget(self.copyLabel)
        self.modeLayout.addWidget(self.copyContainer)

        # USVFS
        self.usvfsContainer = QtWidgets.QWidget(self.modeContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usvfsContainer.sizePolicy().hasHeightForWidth())
        self.usvfsContainer.setSizePolicy(sizePolicy)
        self.usvfsContainer.setObjectName("usvfsContainer")
        self.usvfsLayout = QtWidgets.QHBoxLayout(self.usvfsContainer)
        self.usvfsLayout.setContentsMargins(0, 0, 0, 0)
        self.usvfsLayout.setSpacing(5)
        self.usvfsLayout.setObjectName("usvfsLayout")
        self.usvfsButton = QtWidgets.QRadioButton(self.usvfsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usvfsButton.sizePolicy().hasHeightForWidth())
        self.usvfsButton.setSizePolicy(sizePolicy)
        self.usvfsButton.setMinimumSize(QtCore.QSize(100, 0))
        self.usvfsButton.setObjectName("usvfsButton")        
        self.usvfsButton.setText("USVFS")
        self.usvfsButton.clicked.connect(self.usvfsModeChanged)
        self.usvfsLayout.addWidget(self.usvfsButton)
        self.usvfsLabel = QtWidgets.QLabel(self.usvfsContainer)
        self.usvfsLabel.setWordWrap(True)
        self.usvfsLabel.setObjectName("usvfsLabel")        
        self.usvfsLabel.setText("Uses Mod Organizer\'s virtual file system to add root files to the game folder when running an application. Poor support for exe and dll files.")
        self.usvfsLayout.addWidget(self.usvfsLabel)
        self.modeLayout.addWidget(self.usvfsContainer)

        # USVFS + Links
        self.linkContainer = QtWidgets.QWidget(self.modeContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linkContainer.sizePolicy().hasHeightForWidth())
        self.linkContainer.setSizePolicy(sizePolicy)
        self.linkContainer.setObjectName("linkContainer")
        self.linkLayout = QtWidgets.QHBoxLayout(self.linkContainer)
        self.linkLayout.setContentsMargins(0, 0, 0, 0)
        self.linkLayout.setSpacing(5)
        self.linkLayout.setObjectName("linkLayout")
        self.linkButton = QtWidgets.QRadioButton(self.linkContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linkButton.sizePolicy().hasHeightForWidth())
        self.linkButton.setSizePolicy(sizePolicy)
        self.linkButton.setMinimumSize(QtCore.QSize(100, 0))
        self.linkButton.setObjectName("linkButton")
        self.linkButton.setText("USVFS + Links")
        self.linkButton.clicked.connect(self.linkModeChanged)
        self.linkLayout.addWidget(self.linkButton)
        self.linkLabel = QtWidgets.QLabel(self.linkContainer)
        self.linkLabel.setWordWrap(True)
        self.linkLabel.setObjectName("linkLabel")
        self.linkLabel.setText("USVFS mode. Building creates links for specific root files to improve support for exe and dll files.")
        self.linkLayout.addWidget(self.linkLabel)
        self.modeLayout.addWidget(self.linkContainer)

        self.dialogLayout.addWidget(self.modeContainer)

        # Settings
        self.settingsContainer = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.settingsContainer.sizePolicy().hasHeightForWidth())
        self.settingsContainer.setSizePolicy(sizePolicy)
        self.settingsContainer.setObjectName("settingsContainer")
        self.settingsLayout = QtWidgets.QVBoxLayout(self.settingsContainer)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout.setSpacing(0)
        self.settingsLayout.setObjectName("settingsLayout")
        self.settingsLabel = QtWidgets.QLabel(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsLabel.sizePolicy().hasHeightForWidth())
        self.settingsLabel.setSizePolicy(sizePolicy)
        self.settingsLabel.setObjectName("settingsLabel")        
        self.settingsLabel.setText("<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Settings</span></p></body></html>")
        self.settingsLayout.addWidget(self.settingsLabel)

        # Backup
        self.backupContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backupContainer.sizePolicy().hasHeightForWidth())
        self.backupContainer.setSizePolicy(sizePolicy)
        self.backupContainer.setObjectName("backupContainer")
        self.backupLayout = QtWidgets.QHBoxLayout(self.backupContainer)
        self.backupLayout.setContentsMargins(0, 0, 0, 0)
        self.backupLayout.setObjectName("backupLayout")
        self.backupCheck = QtWidgets.QCheckBox(self.backupContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backupCheck.sizePolicy().hasHeightForWidth())
        self.backupCheck.setSizePolicy(sizePolicy)
        self.backupCheck.setMinimumSize(QtCore.QSize(75, 0))
        self.backupCheck.setObjectName("backupCheck")
        self.backupCheck.setText("Backup")
        self.backupCheck.clicked.connect(self.backupChanged)
        self.backupLayout.addWidget(self.backupCheck)
        self.backupLabel = QtWidgets.QLabel(self.backupContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backupLabel.sizePolicy().hasHeightForWidth())
        self.backupLabel.setSizePolicy(sizePolicy)
        self.backupLabel.setWordWrap(True)
        self.backupLabel.setObjectName("backupLabel")
        self.backupLabel.setText("Root Builder will take a backup of the base game files on the next Build. These files will be used as the source for restoring your game during future Clears.")
        self.backupLayout.addWidget(self.backupLabel)
        self.settingsLayout.addWidget(self.backupContainer)

        # Cache
        self.cacheContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheContainer.sizePolicy().hasHeightForWidth())
        self.cacheContainer.setSizePolicy(sizePolicy)
        self.cacheContainer.setObjectName("cacheContainer")
        self.cacheLayout = QtWidgets.QHBoxLayout(self.cacheContainer)
        self.cacheLayout.setContentsMargins(0, 0, 0, 0)
        self.cacheLayout.setObjectName("cacheLayout")
        self.cacheCheck = QtWidgets.QCheckBox(self.cacheContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheCheck.sizePolicy().hasHeightForWidth())
        self.cacheCheck.setSizePolicy(sizePolicy)
        self.cacheCheck.setMinimumSize(QtCore.QSize(75, 0))
        self.cacheCheck.setObjectName("cacheCheck")
        self.cacheCheck.setText("Cache")
        self.cacheCheck.clicked.connect(self.cacheChanged)
        self.cacheLayout.addWidget(self.cacheCheck)
        self.cacheLabel = QtWidgets.QLabel(self.cacheContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheLabel.sizePolicy().hasHeightForWidth())
        self.cacheLabel.setSizePolicy(sizePolicy)
        self.cacheLabel.setWordWrap(True)
        self.cacheLabel.setObjectName("cacheLabel")
        self.cacheLabel.setText("Root Builder will cache the file hashes of the base game files on the next Build. The hashes are used to detect changes during Sync and Clear.")
        self.cacheLayout.addWidget(self.cacheLabel)
        self.settingsLayout.addWidget(self.cacheContainer)

        # Autobuild
        self.autobuildContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autobuildContainer.sizePolicy().hasHeightForWidth())
        self.autobuildContainer.setSizePolicy(sizePolicy)
        self.autobuildContainer.setObjectName("autobuildContainer")
        self.autobuildLayout = QtWidgets.QHBoxLayout(self.autobuildContainer)
        self.autobuildLayout.setContentsMargins(0, 0, 0, 0)
        self.autobuildLayout.setObjectName("autobuildLayout")
        self.autobuildCheck = QtWidgets.QCheckBox(self.autobuildContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autobuildCheck.sizePolicy().hasHeightForWidth())
        self.autobuildCheck.setSizePolicy(sizePolicy)
        self.autobuildCheck.setMinimumSize(QtCore.QSize(75, 0))
        self.autobuildCheck.setObjectName("autobuildCheck")
        self.autobuildCheck.setText("Autobuild")
        self.autobuildCheck.clicked.connect(self.autobuildChanged)
        self.autobuildLayout.addWidget(self.autobuildCheck)
        self.autobuildLabel = QtWidgets.QLabel(self.autobuildContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autobuildLabel.sizePolicy().hasHeightForWidth())
        self.autobuildLabel.setSizePolicy(sizePolicy)
        self.autobuildLabel.setWordWrap(True)
        self.autobuildLabel.setObjectName("autobuildLabel")
        self.autobuildLabel.setText("When an application is run through Mod Organizer, a Build will run. When that application closes, a Clear will run.")
        self.autobuildLayout.addWidget(self.autobuildLabel)
        self.settingsLayout.addWidget(self.autobuildContainer)

        # Redirect
        self.redirectContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redirectContainer.sizePolicy().hasHeightForWidth())
        self.redirectContainer.setSizePolicy(sizePolicy)
        self.redirectContainer.setObjectName("redirectContainer")
        self.redirectLayout = QtWidgets.QHBoxLayout(self.redirectContainer)
        self.redirectLayout.setContentsMargins(0, 0, 0, 0)
        self.redirectLayout.setObjectName("redirectLayout")
        self.redirectCheck = QtWidgets.QCheckBox(self.redirectContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redirectCheck.sizePolicy().hasHeightForWidth())
        self.redirectCheck.setSizePolicy(sizePolicy)
        self.redirectCheck.setMinimumSize(QtCore.QSize(75, 0))
        self.redirectCheck.setObjectName("redirectCheck")
        self.redirectCheck.setText("Redirect")
        self.redirectCheck.clicked.connect(self.redirectChanged)
        self.redirectLayout.addWidget(self.redirectCheck)
        self.redirectLabel = QtWidgets.QLabel(self.redirectContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.redirectLabel.sizePolicy().hasHeightForWidth())
        self.redirectLabel.setSizePolicy(sizePolicy)
        self.redirectLabel.setWordWrap(True)
        self.redirectLabel.setObjectName("redirectLabel")
        self.redirectLabel.setText("When launching an exe file from a Root folder in a mod, Root Builder will instead launch it from the game folder.")
        self.redirectLayout.addWidget(self.redirectLabel)
        self.settingsLayout.addWidget(self.redirectContainer)

        # Installer
        self.installerContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installerContainer.sizePolicy().hasHeightForWidth())
        self.installerContainer.setSizePolicy(sizePolicy)
        self.installerContainer.setObjectName("installerContainer")
        self.installerLayout = QtWidgets.QHBoxLayout(self.installerContainer)
        self.installerLayout.setContentsMargins(0, 0, 0, 0)
        self.installerLayout.setObjectName("installerLayout")
        self.installerCheck = QtWidgets.QCheckBox(self.installerContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installerCheck.sizePolicy().hasHeightForWidth())
        self.installerCheck.setSizePolicy(sizePolicy)
        self.installerCheck.setMinimumSize(QtCore.QSize(75, 0))
        self.installerCheck.setObjectName("installerCheck")
        self.installerCheck.setText("Installer")
        self.installerCheck.clicked.connect(self.installerChanged)
        self.installerLayout.addWidget(self.installerCheck)
        self.installerLabel = QtWidgets.QLabel(self.installerContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.installerLabel.sizePolicy().hasHeightForWidth())
        self.installerLabel.setSizePolicy(sizePolicy)
        self.installerLabel.setWordWrap(True)
        self.installerLabel.setObjectName("installerLabel")
        self.installerLabel.setText("When installing a mod, Root Builder will attempt to detect if it is a root mod and install it for you. Highly experimental.")
        self.installerLayout.addWidget(self.installerLabel)
        self.settingsLayout.addWidget(self.installerContainer)

        # Text Settings
        self.textSettingContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textSettingContainer.sizePolicy().hasHeightForWidth())
        self.textSettingContainer.setSizePolicy(sizePolicy)
        self.textSettingContainer.setObjectName("textSettingContainer")
        self.textSettingLayout = QtWidgets.QHBoxLayout(self.textSettingContainer)
        self.textSettingLayout.setContentsMargins(0, 0, 0, 0)
        self.textSettingLayout.setSpacing(5)
        self.textSettingLayout.setObjectName("textSettingLayout")

        self.textInputContainer = QtWidgets.QWidget(self.settingsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textInputContainer.sizePolicy().hasHeightForWidth())
        self.textInputContainer.setSizePolicy(sizePolicy)
        self.textInputContainer.setObjectName("textInputContainer")
        self.textInputLayout = QtWidgets.QHBoxLayout(self.textInputContainer)
        self.textInputLayout.setContentsMargins(0, 0, 0, 0)
        self.textInputLayout.setSpacing(5)
        self.textInputLayout.setObjectName("textInputLayout")

        # Exclusions Label
        self.exclusionsLabelContainer = QtWidgets.QWidget(self.textSettingContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exclusionsLabelContainer.sizePolicy().hasHeightForWidth())
        self.exclusionsLabelContainer.setSizePolicy(sizePolicy)
        self.exclusionsLabelContainer.setObjectName("exclusionsLabelContainer")
        self.exclusionsLabelLayout = QtWidgets.QVBoxLayout(self.exclusionsLabelContainer)
        self.exclusionsLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.exclusionsLabelLayout.setSpacing(1)
        self.exclusionsLabelLayout.setObjectName("exclusionsLabelLayout")
        self.exclusionsLabel = QtWidgets.QLabel(self.exclusionsLabelContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exclusionsLabel.sizePolicy().hasHeightForWidth())
        self.exclusionsLabel.setSizePolicy(sizePolicy)
        self.exclusionsLabel.setObjectName("exclusionsLabel")
        self.exclusionsLabel.setText("<html><head/><body><p><span style=\" font-size:9pt;\">Exclusions</span></p></body></html>")
        self.exclusionsLabelLayout.addWidget(self.exclusionsLabel)
        self.exclusionsDescLabel = QtWidgets.QLabel(self.exclusionsLabelContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exclusionsDescLabel.sizePolicy().hasHeightForWidth())
        self.exclusionsDescLabel.setSizePolicy(sizePolicy)
        self.exclusionsDescLabel.setWordWrap(True)
        self.exclusionsDescLabel.setObjectName("exclusionsDescLabel")
        self.exclusionsDescLabel.setText("List of files and folders inside the game directory to be ignored by Root Builder.")
        self.exclusionsLabelLayout.addWidget(self.exclusionsDescLabel)
        self.textSettingLayout.addWidget(self.exclusionsLabelContainer)

        self.exclusionsText = QtWidgets.QLineEdit(self.textInputContainer)
        self.exclusionsText.setObjectName("exclusionsText")
        self.exclusionsText.textChanged.connect(self.exclusionsTextChanged)
        self.textInputLayout.addWidget(self.exclusionsText)

        # Extensions Label
        self.extensionsLabelWidget = QtWidgets.QWidget(self.textSettingContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extensionsLabelWidget.sizePolicy().hasHeightForWidth())
        self.extensionsLabelWidget.setSizePolicy(sizePolicy)
        self.extensionsLabelWidget.setObjectName("extensionsLabelWidget")
        self.extensionsLayout = QtWidgets.QVBoxLayout(self.extensionsLabelWidget)
        self.extensionsLayout.setContentsMargins(0, 0, 0, 0)
        self.extensionsLayout.setSpacing(1)
        self.extensionsLayout.setObjectName("extensionsLayout")
        self.extensionsLabel = QtWidgets.QLabel(self.extensionsLabelWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extensionsLabel.sizePolicy().hasHeightForWidth())
        self.extensionsLabel.setSizePolicy(sizePolicy)
        self.extensionsLabel.setObjectName("extensionsLabel")
        self.extensionsLabel.setText("<html><head/><body><p><span style=\" font-size:9pt;\">Link Extensions</span></p></body></html>")
        self.extensionsLayout.addWidget(self.extensionsLabel)
        self.extensionsDescLabel = QtWidgets.QLabel(self.extensionsLabelWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extensionsDescLabel.sizePolicy().hasHeightForWidth())
        self.extensionsDescLabel.setSizePolicy(sizePolicy)
        self.extensionsDescLabel.setWordWrap(True)
        self.extensionsDescLabel.setObjectName("extensionsDescLabel")
        self.extensionsDescLabel.setText("List of file extensions to create links for when using Link mode.")
        self.extensionsLayout.addWidget(self.extensionsDescLabel)
        self.textSettingLayout.addWidget(self.extensionsLabelWidget)
        
        self.linkText = QtWidgets.QLineEdit(self.textInputContainer)
        self.linkText.setObjectName("linkText")
        self.linkText.textChanged.connect(self.linkExtensionsChanged)
        self.textInputLayout.addWidget(self.linkText)

        self.settingsLayout.addWidget(self.textSettingContainer)
        self.settingsLayout.addWidget(self.textInputContainer)
        self.dialogLayout.addWidget(self.settingsContainer)
        
        # Actions
        self.actionsContainer = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionsContainer.sizePolicy().hasHeightForWidth())
        self.actionsContainer.setSizePolicy(sizePolicy)
        self.actionsContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.actionsContainer.setObjectName("actionsContainer")
        self.actionsLayout = QtWidgets.QHBoxLayout(self.actionsContainer)
        self.actionsLayout.setContentsMargins(0, 0, 0, 0)
        self.actionsLayout.setSpacing(5)
        self.actionsLayout.setObjectName("actionsLayout")

        # Build
        self.buildButton = QtWidgets.QPushButton(self.actionsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildButton.sizePolicy().hasHeightForWidth())
        self.buildButton.setSizePolicy(sizePolicy)
        self.buildButton.setIcon(self.icons.plusIcon())
        self.buildButton.setObjectName("buildButton")
        self.buildButton.setText("Build")
        self.buildButton.clicked.connect(self.buildClick)
        self.actionsLayout.addWidget(self.buildButton)

        # Sync
        self.syncButton = QtWidgets.QPushButton(self.actionsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncButton.sizePolicy().hasHeightForWidth())
        self.syncButton.setSizePolicy(sizePolicy)
        self.syncButton.setIcon(self.icons.syncIcon())
        self.syncButton.setObjectName("syncButton")
        self.syncButton.setText("Sync")
        self.syncButton.clicked.connect(self.syncClick)
        self.actionsLayout.addWidget(self.syncButton)

        # Clear
        self.clearButton = QtWidgets.QPushButton(self.actionsContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setIcon(self.icons.minusIcon())
        self.clearButton.setObjectName("clearButton")
        self.clearButton.setText("Clear")
        self.clearButton.clicked.connect(self.clearClick)
        self.actionsLayout.addWidget(self.clearButton)

        self.dialogLayout.addWidget(self.actionsContainer)

        # Utilities
        self.utilitiesContainer = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.utilitiesContainer.sizePolicy().hasHeightForWidth())
        self.utilitiesContainer.setSizePolicy(sizePolicy)
        self.utilitiesContainer.setObjectName("utilitiesContainer")
        self.utilitiesLayout = QtWidgets.QHBoxLayout(self.utilitiesContainer)
        self.utilitiesLayout.setContentsMargins(0, 0, 0, 0)
        self.utilitiesLayout.setSpacing(5)
        self.utilitiesLayout.setObjectName("utilitiesLayout")

        # Backup
        self.backupButton = QtWidgets.QPushButton(self.utilitiesContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.MinimumExpanding, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backupButton.sizePolicy().hasHeightForWidth())
        self.backupButton.setSizePolicy(sizePolicy)
        self.backupButton.setIcon(self.icons.installIcon())
        self.backupButton.setObjectName("backupButton")
        self.backupButton.setText("Create Backup")
        self.backupButton.clicked.connect(self.backupClick)
        self.utilitiesLayout.addWidget(self.backupButton)

        # Delete Backup
        self.delBackupButton = QtWidgets.QPushButton(self.utilitiesContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.MinimumExpanding, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delBackupButton.sizePolicy().hasHeightForWidth())
        self.delBackupButton.setSizePolicy(sizePolicy)
        self.delBackupButton.setIcon(self.icons.trashIcon())
        self.delBackupButton.setObjectName("delBackupButton")
        self.delBackupButton.setText("Delete Backup")
        self.delBackupButton.clicked.connect(self.delBackupClick)
        self.utilitiesLayout.addWidget(self.delBackupButton)

        # Cache
        self.cacheButton = QtWidgets.QPushButton(self.utilitiesContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.MinimumExpanding, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheButton.sizePolicy().hasHeightForWidth())
        self.cacheButton.setSizePolicy(sizePolicy)
        self.cacheButton.setIcon(self.icons.installIcon())
        self.cacheButton.setObjectName("cacheButton")
        self.cacheButton.setText("Create Cache")
        self.cacheButton.clicked.connect(self.cacheClick)
        self.utilitiesLayout.addWidget(self.cacheButton)

        # Delete Cache
        self.delCacheButton = QtWidgets.QPushButton(self.utilitiesContainer)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.MinimumExpanding, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delCacheButton.sizePolicy().hasHeightForWidth())
        self.delCacheButton.setSizePolicy(sizePolicy)
        self.delCacheButton.setIcon(self.icons.trashIcon())
        self.delCacheButton.setObjectName("delCacheButton")
        self.delCacheButton.setText("Delete Cache")
        self.delCacheButton.clicked.connect(self.delCacheClick)
        self.utilitiesLayout.addWidget(self.delCacheButton)

        self.dialogLayout.addWidget(self.utilitiesContainer)

        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []

    def icon(self):
        return self.icons.linkAltIcon()

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
            self.redirectCheck.setEnabled(True)
            self.autobuildCheck.setEnabled(True)
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
            self.autobuildCheck.setChecked(True)
            self.autobuildCheck.setEnabled(False)
            if not self.rootBuilder.settings.linkmode():
                self.redirectCheck.setEnabled(False)
            else:
                self.redirectCheck.setEnabled(True)
                
        if self.rootBuilder.copier.hasModData() or self.rootBuilder.paths.rootLinkDataFilePath().exists():
            self.backupButton.setEnabled(False)
            self.delBackupButton.setEnabled(False)
            self.cacheButton.setEnabled(False)
            self.delCacheButton.setEnabled(False)
        else:
            if self.rootBuilder.paths.rootCacheFilePath().exists():
                self.delCacheButton.setEnabled(True)
            else:
                self.delCacheButton.setEnabled(False)
            if len(self.rootBuilder.files.getFolderFileList(self.rootBuilder.paths.rootBackupPath())) > 0:
                self.delBackupButton.setEnabled(True)
            else:
                self.delBackupButton.setEnabled(False)

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
        self.bindActions()

    def cacheClick(self):
        self.rootBuilder.backup.buildCache()
        self.bindActions()
    
    def delBackupClick(self):
        self.rootBuilder.backup.clearAllBackupFiles()
        self.rootBuilder.backup.clearFileData()
        self.bindActions()

    def delCacheClick(self):
        self.rootBuilder.backup.clearAllCache()
        self.bindActions()

    def cacheChanged(self):
        self.updateSetting("cache", self.cacheCheck.isChecked())
    
    def backupChanged(self):
        self.updateSetting("backup", self.backupCheck.isChecked())

    def autobuildChanged(self):
        self.updateSetting("autobuild", self.autobuildCheck.isChecked())

    def redirectChanged(self):
        self.updateSetting("redirect", self.redirectCheck.isChecked())

    def installerChanged(self):
        self.updateSetting("installer", self.installerCheck.isChecked())

    def copyModeChanged(self):
        if self.copyButton.isChecked():
            self.updateSetting("usvfsmode", False)
            self.updateSetting("linkmode", False)
            self.autobuildCheck.setEnabled(True)
            self.linkText.setEnabled(False)
            self.usvfsButton.setChecked(False)
            self.linkButton.setChecked(False)
            self.bindActions()

    def usvfsModeChanged(self):
        if self.usvfsButton.isChecked():
            self.updateSetting("usvfsmode", True)
            self.updateSetting("linkmode", False)
            self.updateSetting("autobuild", True)
            self.autobuildCheck.setChecked(True)
            self.autobuildCheck.setEnabled(False)
            self.linkText.setEnabled(False)
            self.copyButton.setChecked(False)
            self.linkButton.setChecked(False)
            self.bindActions()

    def linkModeChanged(self):
        if self.linkButton.isChecked():
            self.updateSetting("usvfsmode", True)
            self.updateSetting("linkmode", True)
            self.updateSetting("autobuild", True)
            self.autobuildCheck.setChecked(True)
            self.autobuildCheck.setEnabled(False)
            self.linkText.setEnabled(True)
            self.copyButton.setChecked(False)
            self.usvfsButton.setChecked(False)
            self.bindActions()

    def exclusionsTextChanged(self):
        self.updateSetting("exclusions", self.exclusionsText.text())

    def linkExtensionsChanged(self):
        self.updateSetting("linkextensions", self.linkText.text())

    def updateSetting(self, name, value):
        self.organiser.setPluginSetting(self.pluginName, name, value)
        