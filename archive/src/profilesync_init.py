import mobase
from .profilesync.plugins.profilesync_tool_manage import ProfileSyncManageTool

def createPlugins():
    return [
        ProfileSyncManageTool()
        ]