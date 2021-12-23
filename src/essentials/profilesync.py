from ..profilesync.plugins.profilesync_tool_manage import ProfileSyncManageTool
import mobase

class ProfileSyncEssentials(ProfileSyncManageTool):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def displayName(self):
        return "Essentials/" + self.baseDisplayName()