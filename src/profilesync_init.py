from .plugin.profilesync.plugins.profilesync_manager import ProfileSyncManager
from .plugin.profilesync.plugins.profilesync_updater import ProfileSyncUpdater

def createPlugins():
    return [
        ProfileSyncManager(),
        ProfileSyncUpdater()
    ]