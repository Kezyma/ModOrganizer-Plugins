try:
    from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
    from PyQt5.QtCore import QCoreApplication, qInfo, QSize, QStandardPaths
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtWidgets import QFileIconProvider
    qtHorizontal = QtCore.Qt.Horizontal
    qtCancel = QtWidgets.QDialogButtonBox.Cancel
    qtOkay = QtWidgets.QDialogButtonBox.Ok
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy
    qtItemView = QtWidgets.QAbstractItemView
    qtItemFlag = QtCore.Qt
    qtCheckState = QtCore.Qt
    qtMatchFlag = QtCore.Qt
except:
    from PyQt6.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
    from PyQt6.QtCore import QCoreApplication, qInfo, QSize, QStandardPaths
    from PyQt6 import QtGui, QtWidgets, QtCore
    from PyQt6.QtWidgets import QFileIconProvider
    qtHorizontal = QtCore.Qt.Orientation.Horizontal
    qtCancel = QtWidgets.QDialogButtonBox.StandardButton.Cancel
    qtOkay = QtWidgets.QDialogButtonBox.StandardButton.Ok
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy.Policy
    qtItemView = QtWidgets.QAbstractItemView.SelectionMode
    qtItemFlag = QtCore.Qt.ItemFlag
    qtCheckState = QtCore.Qt.CheckState
    qtMatchFlag = QtCore.Qt.MatchFlag
from ..openmwplayer_plugin import OpenMWPlayerPlugin
from ...shared.shared_icons import SharedIcons
import mobase, re

class OpenMWPlayerManageTool(OpenMWPlayerPlugin, mobase.IPluginTool):
    
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []

    def icon(self):
        return self.icons.openMwIcon()

    def name(self):
        return self.baseName() + " Manage Tool"
        
    def description(self):
        return self.__tr("Manage OpenMW Player settings.")

    def display(self):
        self.dialog.show()
        self.bindPlugins()

    def bindPlugins(self):
        self.addText.setText(str(self.openMWPlayer.paths.openMWCfgPath()))
        self.dummyCheck.setChecked(self.openMWPlayer.settings.dummyesp())

        profile = self.organiser.profile().name()
        groundCoverCustom = self.openMWPlayer.paths.openMwGrassSettingsPath(profile)
        groundCoverFiles = []
        if not groundCoverCustom.exists():
            with groundCoverCustom.open("x") as custNew:
                custNew.write("\n")
        with groundCoverCustom.open("r") as custGrnd:
            for line in custGrnd:
                line = line.replace("\n", "")
                if len(line) > 0:
                    groundCoverFiles.append(line)
                    
        self.profileSelect.clear()
        for name in self.organiser.pluginList().pluginNames():
            item = QtWidgets.QListWidgetItem()
            item.setText(name)
            item.setFlags(qtItemFlag.ItemIsUserCheckable|qtItemFlag.ItemIsEnabled)
            item.setCheckState(qtCheckState.Unchecked)
            self.profileSelect.addItem(item)
            
        for name in groundCoverFiles:
            for itm in self.profileSelect.findItems(name, qtMatchFlag.MatchExactly):
                itm.setCheckState(qtCheckState.Checked)

    def dummyEspCheck(self):
        self.organiser.setPluginSetting(self.baseName(), "dummyesp", self.dummyCheck.isChecked())
        if self.dummyCheck.isChecked():
            self.openMWPlayer.enableDummy()
        else:
            self.openMWPlayer.disableDummy()

    def selectOpenMWCfg(self):
        manualPath = QFileDialog.getOpenFileName(self._parentWidget(), self.__tr("Locate OpenMW Config File"), ".", "OpenMW Config File (openmw.cfg)")[0]
        self.organiser.setPluginSetting(self.baseName(), "openmwcfgpath", str(manualPath))
        self.addText.setText(str(manualPath))

    def changePluginState(self):
        selected = []
        for x in range(self.profileSelect.count()):
            p = self.profileSelect.item(x)
            if p.checkState() == qtCheckState.Checked:
                selected.append(p.text())
        
        profile = self.organiser.profile().name()
        groundCoverCustom = self.openMWPlayer.paths.openMwGrassSettingsPath(profile)
        with groundCoverCustom.open("w") as custGrnd:
            for item in selected:
                custGrnd.write(item + "\n")

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setObjectName("dialog")
        dialog.resize(475, 340)
        dialog.setWindowIcon(self.icons.openMwIcon())
        dialog.setWindowTitle("OpenMW Player")
        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setContentsMargins(5, 5, 5, 5)
        self.dialogLayout.setSpacing(5)
        self.dialogLayout.setObjectName("dialogLayout")

        self.addWidget = QtWidgets.QWidget(dialog)
        self.addWidget.setObjectName("addWidget")
        self.addLayout = QtWidgets.QHBoxLayout(self.addWidget)
        self.addLayout.setContentsMargins(0, 0, 0, 0)
        self.addLayout.setSpacing(5)
        self.addLayout.setObjectName("addLayout")
        self.addText = QtWidgets.QLabel(self.addWidget)
        self.addText.setObjectName("addText")
        self.addButton = QtWidgets.QPushButton(self.addWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setIcon(self.icons.linkIcon())
        self.addButton.setObjectName("addButton")
        self.addButton.setText("OpenMW.cfg")
        self.addButton.clicked.connect(self.selectOpenMWCfg)
        self.addLayout.addWidget(self.addButton)
        self.addLayout.addWidget(self.addText)
        self.dialogLayout.addWidget(self.addWidget)

        self.dummyWidget = QtWidgets.QWidget(dialog)
        self.dummyWidget.setObjectName("dummyWidget")
        self.dummyLayout = QtWidgets.QHBoxLayout(self.dummyWidget)
        self.dummyLayout.setContentsMargins(0, 0, 0, 0)
        self.dummyLayout.setSpacing(5)
        self.dummyLayout.setObjectName("dummyLayout")
        #self.dummyText = QtWidgets.QLabel(self.dummyWidget)
        #self.dummyText.setObjectName("dummyText")

        self.dummyCheck = QtWidgets.QCheckBox(self.dummyWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dummyCheck.sizePolicy().hasHeightForWidth())
        self.dummyCheck.setSizePolicy(sizePolicy)
        self.dummyCheck.setMinimumSize(QtCore.QSize(75, 0))
        self.dummyCheck.setObjectName("dummyCheck")
        self.dummyCheck.setText("Enable omwaddon and omwscripts support via esp files.")
        self.dummyCheck.clicked.connect(self.dummyEspCheck)
        self.dummyLayout.addWidget(self.dummyCheck)

        #self.dummyLayout.dummyWidget(self.dummyText)
        self.dialogLayout.addWidget(self.dummyWidget)

        self.gcvWidget = QtWidgets.QWidget(dialog)
        self.gcvWidget.setObjectName("gcvWidget")
        self.gcvLayout = QtWidgets.QHBoxLayout(self.gcvWidget)
        self.gcvLayout.setContentsMargins(0, 0, 0, 0)
        self.gcvLayout.setSpacing(5)
        self.gcvLayout.setObjectName("gcvLayout")
        self.gcvText = QtWidgets.QLabel(self.gcvWidget)
        self.gcvText.setText("Select Groundcover Plugins")
        self.gcvText.setObjectName("gcvText")
        self.gcvLayout.addWidget(self.gcvText)
        self.dialogLayout.addWidget(self.gcvWidget)

        self.profileSelect = QtWidgets.QListWidget(dialog)
        self.profileSelect.setSelectionMode(qtItemView.MultiSelection)
        self.profileSelect.setObjectName("profileSelect")
        self.profileSelect.itemChanged.connect(self.changePluginState)
        self.dialogLayout.addWidget(self.profileSelect)

        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog