import mobase
from ..core.profilesync_plugin import ProfileSyncPlugin
from ..modules.profilesync_menu import ProfileSyncMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *

class ProfileSyncManager(ProfileSyncPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        self._organiser.onProfileChanged(self.changeProfile)
        self._organiser.onProfileRemoved(self.removeProfile)
        self._organiser.onProfileRenamed(self.renameProfile)
        self._organiser.modList().onModInstalled(self.syncCurrent)
        self._organiser.modList().onModMoved(self.syncCurrent)
        self._organiser.modList().onModRemoved(self.syncCurrent)
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    #def master(self):
    #    return self._pluginName

    #def settings(self):
    #    return []

    def icon(self):
        return self._icons.syncIcon()

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Manage Profile Sync groups.")
    
    def display(self):
        self._dialog.show()
        #self._profileSyncMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), f"v{self.version().displayString()}", self.icon())
        self._profileSyncMenu = ProfileSyncMenu(dialog, self._organiser, self._profileSync)
        dialog.addContent(self._profileSyncMenu)
        return dialog

    def sync(self, profile:str):
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            self._profileSync._sync.syncFromProfile(profile)
            self._profileSync._sync.syncFromGroup(group)

    def syncCurrent(self):
        profile = self._organiser.profile().name()
        self.sync(profile)

    def renameProfile(self, profile:mobase.IProfile, oldName:str, newName:str):
        self._profileSync._groups.renameProfile(oldName, newName)

    def removeProfile(self, profile:str):
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            groupList = self._profileSync._groups.loadSyncGroups()
            groupProfiles = groupList[group]
            groupProfiles.pop(groupProfiles.index(profile))
            groupList[group] = groupProfiles
            self._profileSync._groups.saveSyncGroups(groupList)

    def changeProfile(self, oldProfile:mobase.IProfile, newProfile:mobase.IProfile):
        if oldProfile is not None:
            oldName = oldProfile.name()
            self.sync(oldName)

