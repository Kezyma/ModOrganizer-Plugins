import mobase
from ...shared.shared_files import SharedFiles

class ProfileSyncFiles(SharedFiles):
    """ Profile Sync file module. Used to get collections of files from different game paths. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("ProfileSync", organiser) 