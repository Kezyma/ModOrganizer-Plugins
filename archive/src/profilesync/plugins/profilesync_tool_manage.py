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
    qtItemView = QtWidgets.QAbstractItemView
    qtItemFlag = QtCore.Qt
    qtCheckState = QtCore.Qt
    qtMatchFlag = QtCore.Qt
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
    qtItemView = QtWidgets.QAbstractItemView.SelectionMode
    qtItemFlag = QtCore.Qt.ItemFlag
    qtCheckState = QtCore.Qt.CheckState
    qtMatchFlag = QtCore.Qt.MatchFlag
from ..profilesync_plugin import ProfileSyncPlugin
import mobase, re

class ProfileSyncManageTool(ProfileSyncPlugin, mobase.IPluginTool):
    
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        self.organiser.onProfileRenamed(lambda prof, old, new: self.profileRename(old, new)) # need to find the profile in current sync groups and change name.
        self.organiser.modList().onModMoved(lambda mod, old, new: self.syncProfile()) # need to get the profile modlist, sync it if applicable.
        self.organiser.modList().onModInstalled(lambda mod: self.syncProfile())
        self.organiser.modList().onModRemoved(lambda mod: self.syncProfile())
        self.organiser.onProfileChanged(lambda old, new: self.loadProfile(new.name()))
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.syncIcon()
        
    def description(self):
        return self.__tr("Manage Profile Sync groups.")

    def display(self):
        self.dialog.show()
        self.bindProfiles()
        self.bindSyncGroups()

    def loadProfile(self, profileName=str):
        self.profilesync.groupToProfile(self.profilesync.getProfileGroup(profileName), profileName)

    def profileRename(self, oldName, newName):
        self.profilesync.renameProfile(oldName, newName)
        
    def syncProfile(self):
        self.profilesync.syncFromCurrent()

    def checkGroupName(self):
        if self.addText.text().strip() == "" or self.addText.text().lower().strip() in [x.lower().strip() for x in self.profilesync.getSyncGroups().keys()]:
            self.addButton.setEnabled(False)
        else:
            self.addButton.setEnabled(True)

    def bindGroup(self):
        group = self.syncSelect.currentText()
        self.profileSelect.blockSignals(True)
        if group and group != "":
            profiles = self.profilesync.getSyncGroups()[group]["Profiles"]
            disabled = self.profilesync.groupedProfiles(group)
            self.bindProfiles()
            for d in disabled:
                self.disableProfile(d)
            for p in profiles:
                self.checkProfile(p)
        else:
            self.bindProfiles()
            profiles = self.profilesync.files.getFileNamesFromList(self.profilesync.files.getSubFolderList(self.profilesync.paths.modOrganizerProfilesPath(), False))
            for p in profiles:
                self.disableProfile(p)
        self.profileSelect.blockSignals(False)

    def updateProfiles(self):
        items = []
        selected = []
        for x in range(self.profileSelect.count()):
            p = self.profileSelect.item(x)
            items.append(p.text())
            if p.checkState() == qtCheckState.Checked:
                selected.append(p.text())
        for item in items:
            enabled = False
            for select in selected:
                if select == item:
                    enabled = True
            if enabled:
                self.profilesync.addProfileToGroup(self.syncSelect.currentText(), item)
            else:
                self.profilesync.removeProfileFromGroup(self.syncSelect.currentText(), item)

    def addGroup(self):
        self.profilesync.addSyncGroup(self.addText.text())
        self.addText.setText("")
        self.checkGroupName()
        self.bindSyncGroups()

    def deleteGroup(self):
        self.profilesync.removeSyncGroup(self.syncSelect.currentText())
        self.bindSyncGroups()

    def bindSyncGroups(self):
        self.syncSelect.clear()
        self.syncSelect.addItems(self.profilesync.getSyncGroups().keys())
        self.bindGroup()

    def bindProfiles(self):
        self.profileSelect.clear()
        profiles = self.profilesync.files.getFileNamesFromList(self.profilesync.files.getSubFolderList(self.profilesync.paths.modOrganizerProfilesPath(), False))
        for profile in profiles:
            self.addProfile(profile)

    def enableProfile(self, profileName=str):
        for itm in self.profileSelect.findItems(profileName, qtMatchFlag.MatchExactly):
            itm.setFlags(qtItemFlag.ItemIsUserCheckable|qtItemFlag.ItemIsEnabled)

    def disableProfile(self, profileName=str):
        for itm in self.profileSelect.findItems(profileName, qtMatchFlag.MatchExactly):
            itm.setFlags(qtItemFlag.ItemIsUserCheckable)

    def checkProfile(self, profileName=str):
        for itm in self.profileSelect.findItems(profileName, qtMatchFlag.MatchExactly):
            itm.setCheckState(qtCheckState.Checked)

    def uncheckProfile(self, profileName=str):
        for itm in self.profileSelect.findItems(profileName, qtMatchFlag.MatchExactly):
            itm.setCheckState(qtCheckState.Unchecked)

    def addProfile(self, profileName=str):
        item = QtWidgets.QListWidgetItem()
        item.setText(profileName)
        item.setFlags(qtItemFlag.ItemIsUserCheckable|qtItemFlag.ItemIsEnabled)
        item.setCheckState(qtCheckState.Unchecked)
        self.profileSelect.addItem(item)

        __sortingEnabled = self.profileSelect.isSortingEnabled()
        self.profileSelect.setSortingEnabled(False)
        self.profileSelect.setSortingEnabled(__sortingEnabled)

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setObjectName("dialog")
        dialog.resize(475, 340)
        dialog.setWindowIcon(self.icons.syncIcon())
        dialog.setWindowTitle("Profile Sync")
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
        self.addLabel = QtWidgets.QLabel(self.addWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addLabel.sizePolicy().hasHeightForWidth())
        self.addLabel.setSizePolicy(sizePolicy)
        self.addLabel.setObjectName("addLabel")
        self.addLabel.setText("New Sync Group")
        self.addLayout.addWidget(self.addLabel)
        self.addText = QtWidgets.QLineEdit(self.addWidget)
        self.addText.setObjectName("addText")
        self.addText.setPlaceholderText("Name")
        self.addText.textChanged.connect(self.checkGroupName)
        self.addLayout.addWidget(self.addText)
        self.addButton = QtWidgets.QPushButton(self.addWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setIcon(self.icons.plusIcon())
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.addButton.clicked.connect(self.addGroup)
        self.addLayout.addWidget(self.addButton)
        self.dialogLayout.addWidget(self.addWidget)

        self.selectWidget = QtWidgets.QWidget(dialog)
        self.selectWidget.setObjectName("selectWidget")
        self.selectLayout = QtWidgets.QHBoxLayout(self.selectWidget)
        self.selectLayout.setContentsMargins(0, 0, 0, 0)
        self.selectLayout.setSpacing(5)
        self.selectLayout.setObjectName("selectLayout")
        self.syncSelect = QtWidgets.QComboBox(self.selectWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.syncSelect.sizePolicy().hasHeightForWidth())
        self.syncSelect.setSizePolicy(sizePolicy)
        self.syncSelect.setObjectName("syncSelect")
        self.syncSelect.currentTextChanged.connect(self.bindGroup)
        self.selectLayout.addWidget(self.syncSelect)
        self.deleteButton = QtWidgets.QPushButton(self.selectWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        self.deleteButton.setIcon(self.icons.trashIcon())
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Delete")
        self.deleteButton.clicked.connect(self.deleteGroup)
        self.selectLayout.addWidget(self.deleteButton)
        self.dialogLayout.addWidget(self.selectWidget)

        self.profileSelect = QtWidgets.QListWidget(dialog)
        self.profileSelect.setSelectionMode(qtItemView.MultiSelection)
        self.profileSelect.setObjectName("profileSelect")
        self.profileSelect.itemChanged.connect(self.updateProfiles)
        self.dialogLayout.addWidget(self.profileSelect)

        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog



        
        
