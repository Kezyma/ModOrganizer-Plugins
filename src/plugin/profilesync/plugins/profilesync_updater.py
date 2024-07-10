import mobase
from ..core.profilesync_plugin import ProfileSyncPlugin
from ..models.profilesync_groupdata import *
from ....common.common_qt import *
from threading import Thread

class ProfileSyncUpdater(ProfileSyncPlugin, mobase.IPlugin):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        #self._organiser.onProfileChanged(lambda old, new: self.changeProfile(old, new))
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
        self._log.debug(f"Finding the sync group for {profile}.")
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            self._log.debug(f"Found group {group}, updating group modlist.")
            self._profileSync._sync.syncFromProfile(profile)
            self._log.debug(f"Updated group modlist, synchronising other profiles.")
            self._profileSync._sync.syncFromGroup(group)
        else:
            self._log.debug(f"No group found for {profile}.")

    def syncFromCurrent(self):
        self._profileSync._legacy.migrate()
        profile = self._organiser.profile().name()
        self._log.debug(f"Finding the sync group for {profile}.")
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            self._log.debug(f"Found group {group}, updating group modlist.")
            self._profileSync._sync.syncFromCurrentProfile()
            self._log.debug(f"Updated group modlist, synchronising other profiles.")
            if self._profileSync._settings.useasync():
                t = Thread(target=self._profileSync._sync.syncFromGroup, args=[group])
                t.start()
            else:
                self._profileSync._sync.syncFromGroup(group)
        else:
            self._log.debug(f"No group found for {profile}.")

    def renameProfile(self, profile:mobase.IProfile, oldName:str, newName:str):
        self._log.debug(f"Renaming {oldName} to {newName} in any sync groups.")
        self._profileSync._groups.renameProfile(oldName, newName)

    def removeProfile(self, profile:str):
        self._log.debug(f"Removing {profile} from any sync groups.")
        group = self._profileSync._groups.groupFromProfile(profile)
        if group is not None:
            groupList = self._profileSync._groups.loadSyncGroups()
            groupProfiles = groupList[group]
            groupProfiles[PROFILES].pop(groupProfiles[PROFILES].index(profile))
            groupList[group] = groupProfiles
            self._profileSync._groups.saveSyncGroups(groupList)

    def changeProfile(self, oldProfile:mobase.IProfile, newProfile:mobase.IProfile):
        if oldProfile is not None:
            oldName = oldProfile.name()
            self._log.debug(f"Switching profile, synchronising {oldName}")
            self.sync(oldName)


