from ....common import common_icons
from ....common.common_qt import *
from ....common.common_utilities import deleteFile
from ..core.profilesync import ProfileSync
from .profilesync_update import ProfileSyncUpdate
import mobase, webbrowser, os
from pathlib import Path

try:
    from ..ui.qt6.profilesync_menu import Ui_profileSyncMenuWidget
    from ..ui.qt6.profilesync_groups import Ui_profileSyncGroupsTabWidget
    from ..ui.qt6.profilesync_states import Ui_groupSyncWidget
    from ..ui.qt6.profilesync_select import Ui_profileSelectWidget
    from ..ui.qt6.profilesync_update import Ui_updateTabWidget
except:
    from ..ui.qt5.profilesync_menu import Ui_profileSyncMenuWidget
    from ..ui.qt5.profilesync_groups import Ui_profileSyncGroupsTabWidget
    from ..ui.qt5.profilesync_states import Ui_groupSyncWidget
    from ..ui.qt5.profilesync_select import Ui_profileSelectWidget
    from ..ui.qt5.profilesync_update import Ui_updateTabWidget

class ProfileSyncMenu(QtWidgets.QWidget):
    """Profile Sync menu widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, profileSync:ProfileSync, update:ProfileSyncUpdate):
        super().__init__(parent)
        self._organiser = organiser
        self._profileSync = profileSync
        self._update = update
        self._rebind = False
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_profileSyncMenuWidget()
        self.widget.setupUi(self)

        self.groupsTabWidget = Ui_profileSyncGroupsTabWidget()
        self.groupsTabWidget.setupUi(self.widget.groupsTab)
        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)
        self.stateTabWidget = Ui_groupSyncWidget()
        self.stateTabWidget.setupUi(self.widget.stateTab)
        self.selectWidget = Ui_profileSelectWidget()
        self.selectWidget.setupUi(self.widget.groupSelectWidget)
        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)

        self.groupsTabWidget.profileList.itemChanged.connect(self.saveProfileList)
        self.selectWidget.groupSelect.currentTextChanged.connect(self.groupSelect_changed)
        self.selectWidget.groupDeleteButton.clicked.connect(self.deleteGroup_clicked)
        self.selectWidget.newGroupButton.clicked.connect(self.createGroup_clicked)

        self.stateTabWidget.stateGroupSelect.currentTextChanged.connect(self.stateGroupSelect_changed)
        self.stateTabWidget.createStateGroupBtn.clicked.connect(self.createStateGroup_clicked)
        self.stateTabWidget.deleteStateGroupBtn.clicked.connect(self.deleteStateGroup_clicked)
        self.stateTabWidget.stateProfileList.itemChanged.connect(self.saveStateLists)
        self.stateTabWidget.stateCategoryList.itemChanged.connect(self.saveStateLists)

        self.helpTabWidget.discordButton.setIcon(common_icons.DISCORD_ICON)
        self.helpTabWidget.discordButton.clicked.connect(self.discord_clicked)
        self.helpTabWidget.docsButton.setIcon(common_icons.DOCS_ICON)
        self.helpTabWidget.docsButton.clicked.connect(self.docs_clicked)
        self.helpTabWidget.githubButton.setIcon(common_icons.GITHUB_ICON)
        self.helpTabWidget.githubButton.clicked.connect(self.github_clicked)
        self.helpTabWidget.nexusButton.setIcon(common_icons.NEXUS_ICON)
        self.helpTabWidget.nexusButton.clicked.connect(self.nexus_clicked)
        self.helpTabWidget.patreonButton.setIcon(common_icons.PATREON_ICON)
        self.helpTabWidget.patreonButton.clicked.connect(self.patreon_clicked)

        helpPath = Path(__file__).parent.parent / "data" / "profilesync_help.html"
        helpUrl = QtCore.QUrl.fromLocalFile(str(helpPath.absolute()))
        self.helpTabWidget.helpText.setSource(helpUrl)

        self.updateTabWidget.updateFoundWidget.setVisible(False)
        self.updateTabWidget.noUpdateWidget.setVisible(False)
        self.updateTabWidget.checkUpdateButton.setIcon(self._icons.refreshIcon())
        self.updateTabWidget.updateFoundButton.setIcon(self._icons.downloadIcon())
        self.updateTabWidget.updateFoundButton.clicked.connect(self.updateFound_clicked)
        self.updateTabWidget.checkUpdateButton.clicked.connect(self.checkUpdate_clicked)

    def rebind(self):
        """Rebinds the UI with current settings."""
        self.bindSyncGroupList()

    def bindSyncGroupList(self):
        groups = self._profileSync._groups.loadSyncGroups()
        self.selectWidget.groupSelect.clear()
        self.selectWidget.groupSelect.addItems(groups.keys())
        self.bindSyncGroup()

    def bindSyncGroup(self):
        selectedGroup = self.selectWidget.groupSelect.currentText()
        hasSelectedGroup = selectedGroup != ""
        self.selectWidget.groupDeleteButton.setEnabled(hasSelectedGroup)
        self.bindGroupProfiles()
        self.bindStateGroups()

    def bindGroupProfiles(self):
        groups = self._profileSync._groups.loadSyncGroups()
        profilesPath = self._profileSync._strings.moProfilesPath
        profileList = os.listdir(profilesPath)
        self.groupsTabWidget.profileList.clear()
        selectedGroup = self.selectWidget.groupSelect.currentText()
        hasSelectedGroup = selectedGroup != ""
        self.groupsTabWidget.profileList.setEnabled(hasSelectedGroup)
        if hasSelectedGroup:
            disabledProfiles = []
            checkedProfiles = []
            for g in groups:
                if g != selectedGroup:
                    disabledProfiles.extend(groups[g][self._profileSync._groups.PROFILES])
                else:
                    checkedProfiles.extend(groups[g][self._profileSync._groups.PROFILES])
            for p in profileList:
                pItm = QtWidgets.QListWidgetItem()
                pItm.setText(p)
                checked = qCheckState.Unchecked
                if p in checkedProfiles:
                    checked = qCheckState.Checked
                flags = qItemFlag.ItemIsUserCheckable
                if p not in disabledProfiles:
                    flags = flags | qItemFlag.ItemIsEnabled
                pItm.setCheckState(checked)
                pItm.setFlags(flags)
                self.groupsTabWidget.profileList.addItem(pItm)

    def bindStateGroups(self):
        selectedGroup = self.selectWidget.groupSelect.currentText()
        hasSelectedGroup = selectedGroup != ""
        self.stateTabWidget.stateGroupSelect.clear()
        self.widget.stateTab.setEnabled(hasSelectedGroup)
        if hasSelectedGroup:
            syncGroups = self._profileSync._groups.loadSyncGroups()
            stateGroups = syncGroups[selectedGroup][self._profileSync._groups.STATEGROUPS]
            self.stateTabWidget.stateGroupSelect.addItems(stateGroups.keys())
        self.bindStateGroup()

    def bindStateGroup(self):
        selectedGroup = self.selectWidget.groupSelect.currentText()
        hasSelectedGroup = selectedGroup != ""
        selectedState = self.stateTabWidget.stateGroupSelect.currentText()
        hasSelectedState = hasSelectedGroup and selectedState != ""
        self.stateTabWidget.stateProfileList.setEnabled(hasSelectedState)
        self.stateTabWidget.stateCategoryList.setEnabled(hasSelectedState)
        self.stateTabWidget.deleteStateGroupBtn.setEnabled(hasSelectedState)
        if hasSelectedState:
            groups = self._profileSync._groups.loadSyncGroups()
            selectedGroupItm = groups[selectedGroup]
            stateGroups = selectedGroupItm[self._profileSync._groups.STATEGROUPS]
            groupProfiles = selectedGroupItm[self._profileSync._groups.PROFILES]

            profile = self._organiser.profile()
            modList = self._organiser.modList().allModsByProfilePriority(profile)
            listCats = self._profileSync._sync.modlistToCategories(modList)
            categories = listCats.keys()

            selectedStateGroup = stateGroups[selectedState]
            selectedProfiles = selectedStateGroup[self._profileSync._groups.PROFILES]
            selectedCategories = selectedStateGroup[self._profileSync._groups.CATEGORIES]
            invalidProfiles = []
            invalidCategories = []
            for stateGroup in stateGroups:
                if stateGroup != selectedState:
                    for p in selectedProfiles:
                        if p in stateGroups[stateGroup][self._profileSync._groups.PROFILES]:
                            invalidCategories.extend(stateGroups[stateGroup][self._profileSync._groups.CATEGORIES])
                    for c in selectedCategories:
                        if c in stateGroups[stateGroup][self._profileSync._groups.CATEGORIES]:
                            invalidProfiles.extend(stateGroups[stateGroup][self._profileSync._groups.PROFILES])

            self.bindStateProfiles(groupProfiles, selectedProfiles, invalidProfiles)
            self.bindStateCategories(categories, selectedCategories, invalidCategories)

    def bindStateProfiles(self, groupProfiles:list, selectedProfiles:list, invalidProfiles:str):
        self.stateTabWidget.stateProfileList.clear()
        for p in groupProfiles:
            pItm = QtWidgets.QListWidgetItem()
            pItm.setText(p)
            check = qCheckState.Unchecked
            if p in selectedProfiles:
                check = qCheckState.Checked
            flags = qItemFlag.ItemIsUserCheckable 
            if p not in invalidProfiles:
                flags = flags | qItemFlag.ItemIsEnabled
            pItm.setCheckState(check)
            pItm.setFlags(flags)
            self.stateTabWidget.stateProfileList.addItem(pItm)

    def bindStateCategories(self, categories:list, selectedCategories:list, invalidCategories:str):
        self.stateTabWidget.stateCategoryList.clear()
        for c in categories:
            pItm = QtWidgets.QListWidgetItem()
            pItm.setText(c)
            check = qCheckState.Unchecked
            if c in selectedCategories:
                check = qCheckState.Checked
            flags = qItemFlag.ItemIsUserCheckable 
            if c not in invalidCategories:
                flags = flags | qItemFlag.ItemIsEnabled
            pItm.setFlags(flags)
            pItm.setCheckState(check)
            self.stateTabWidget.stateCategoryList.addItem(pItm)

    def createSyncGroup(self):
        newName = self.selectWidget.newGroupText.text()
        if newName != "":
            self._profileSync._groups.createSyncGroup(newName)
            self.bindSyncGroupList()
            self.selectWidget.groupSelect.setCurrentText(newName)
            self.bindSyncGroup()

    def createStateGroup(self):
        selectedGroup = self.selectWidget.groupSelect.currentText()
        hasSelectedGroup = selectedGroup != ""
        newName = self.stateTabWidget.createStateGroupText.text()
        if hasSelectedGroup and newName != "":
            self._profileSync._groups.createStateGroup(selectedGroup, newName)
            self.bindStateGroups()
            self.stateTabWidget.stateGroupSelect.setCurrentText(newName)
            self.bindStateGroup()

    def discord_clicked(self):
        webbrowser.open("https://discord.com/invite/kPA3RrxAYz")

    def docs_clicked(self):
        webbrowser.open("https://kezyma.github.io/?p=profilesync")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/60690")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")

    def updateFound_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/60690?tab=files")

    def createGroup_clicked(self):
        self.createSyncGroup()

    def createStateGroup_clicked(self):
        self.createStateGroup()

    def deleteGroup_clicked(self):
        group = self.selectWidget.groupSelect.currentText()
        if group != "":
            groupList = self._profileSync._groups.loadSyncGroups()
            stateGroups = groupList[group][self._profileSync._groups.STATEGROUPS]
            for sg in stateGroups:
                stateListPath = self._profileSync._groups.stateGroupModlist(group, sg)
                deleteFile(stateListPath)
            groupList.pop(group, None)
            self._profileSync._groups.saveSyncGroups(groupList)
            groupListPath = self._profileSync._groups.groupModlist(group)
            deleteFile(groupListPath)
            self.bindSyncGroupList()

    def deleteStateGroup_clicked(self):
        groupName = self.selectWidget.groupSelect.currentText()
        stateName = self.stateTabWidget.stateGroupSelect.currentText()
        if stateName != "":
            groupList = self._profileSync._groups.loadSyncGroups()
            if groupName in groupList:
                groupList[groupName][self._profileSync._groups.STATEGROUPS].pop(stateName, None)
                stateListPath = self._profileSync._groups.stateGroupModlist(groupName, stateName)
                deleteFile(stateListPath)
                self._profileSync._groups.saveSyncGroups(groupList)
            self.bindStateGroups()

    def groupSelect_changed(self):
        self.bindSyncGroup()

    def stateGroupSelect_changed(self):
        self.bindStateGroup()

    def saveProfileList(self):
        selected = []
        for x in range(self.groupsTabWidget.profileList.count()):
            p = self.groupsTabWidget.profileList.item(x)
            if p.checkState() == qCheckState.Checked:
                selected.append(p.text())
        group = self.selectWidget.groupSelect.currentText()
        groups = self._profileSync._groups.loadSyncGroups()
        groups[group][self._profileSync._groups.PROFILES] = selected
        self._profileSync._groups.saveSyncGroups(groups)

        if len(selected) > 0:
            groupListPath = self._profileSync._groups.groupModlist(group)
            if not Path(groupListPath).exists():
                self._profileSync._sync.syncFromProfile(selected[0])
            else:
                self._profileSync._sync.syncFromGroup(group)
        else:
            groupListPath = self._profileSync._groups.groupModlist(group)
            deleteFile(groupListPath)
            states = groups[group][self._profileSync._groups.STATEGROUPS]
            for s in states:
                stateListPath = self._profileSync._groups.stateGroupModlist(group, s)
                deleteFile(stateListPath)

        self.bindStateGroup()

    def saveStateLists(self):
        selectedProfiles = []
        for x in range(self.stateTabWidget.stateProfileList.count()):
            p = self.stateTabWidget.stateProfileList.item(x)
            if p.checkState() == qCheckState.Checked:
                selectedProfiles.append(p.text())

        selectedCategories = []
        for x in range(self.stateTabWidget.stateCategoryList.count()):
            p = self.stateTabWidget.stateCategoryList.item(x)
            if p.checkState() == qCheckState.Checked:
                selectedCategories.append(p.text())

        selectedGroup = self.selectWidget.groupSelect.currentText()
        selectedState = self.stateTabWidget.stateGroupSelect.currentText()
        self._profileSync._groups.updateStateGroups(selectedGroup, selectedState, selectedProfiles, selectedCategories)

        if len(selectedProfiles) > 0:
            stateListPath = self._profileSync._groups.stateGroupModlist(selectedGroup, selectedState)
            if not Path(stateListPath).exists():
                self._profileSync._sync.syncFromProfile(selectedProfiles[0])
            else:
                self._profileSync._sync.syncFromGroup(selectedGroup)
        else:
            stateListPath = self._profileSync._groups.stateGroupModlist(selectedGroup, selectedState)
            deleteFile(stateListPath)
        
        self.bindStateGroup()

    def checkUpdate_clicked(self):
        """Checks for an update"""
        newVersion = self._update.getLatestVersion()
        hasUpdate = newVersion != None
        self.updateTabWidget.updateFoundWidget.setVisible(hasUpdate)
        self.updateTabWidget.noUpdateWidget.setVisible(not hasUpdate)

    