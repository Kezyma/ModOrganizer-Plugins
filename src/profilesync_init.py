from .plugin.profilesync.plugins.profilesync_manager import ProfileSyncManager

def createPlugins():
    return [
        ProfileSyncManager()
    ]