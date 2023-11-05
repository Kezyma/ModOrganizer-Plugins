import mobase
from ..core.profilesync_plugin import ProfileSyncPlugin
from ....common.common_qt import *
from threading import Thread

class ProfileSyncUpdater(ProfileSyncPlugin, mobase.IPlugin):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._organiser.onProfileChanged(lambda old, new: self.changeProfile(old, new))
        self._organiser.onProfileRemoved(lambda name: self.removeProfile(name))
        self._organiser.onProfileRenamed(lambda profile, old, new: self.renameProfile(profile, old, new))
        self._organiser.modList().onModInstalled(lambda mod: self.syncFromCurrent())
        self._organiser.modList().onModMoved(lambda mod, old, new: self.syncFromCurrent())
        self._organiser.modList().onModRemoved(lambda mod: self.syncFromCurrent())
        self._organiser.modList().onModStateChanged(lambda map: self.syncFromCurrent())
        self._organiser.onUserInterfaceInitialized(lambda window: self.migrate())
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return self._icons.syncIcon()

    def master(self):
        return self._pluginName

    def settings(self):
        return []
    
    def name(self):
        return f"{self.baseName()} Updater"

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Updates profiles and sync groups with changes.")

    def migrate(self):
        self._profileSync._legacy.migrate()

    def sync(self, profile:str):
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            self._profileSync._sync.syncFromProfile(profile)
            self._profileSync._sync.syncFromGroup(group)

    def syncFromCurrent(self):
        self._profileSync._legacy.migrate()
        profile = self._organiser.profile().name()
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            self._profileSync._sync.syncFromCurrentProfile()
            t = Thread(target=self._profileSync._sync.syncFromGroup, args=[group])
            t.start()

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


