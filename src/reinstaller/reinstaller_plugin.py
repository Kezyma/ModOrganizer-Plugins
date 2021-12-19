import mobase 
from ..shared.shared_plugin import SharedPlugin
from .reinstaller import Reinstaller

class ReinstallerPlugin(SharedPlugin):

    def __init__(self):
        super().__init__("Reinstaller", "Reinstaller", mobase.VersionInfo(1,1,0, mobase.ReleaseType.BETA))

    def init(self, organiser=mobase.IOrganizer):
        self.reinstaller = Reinstaller(organiser)
        return super().init(organiser)
    
        