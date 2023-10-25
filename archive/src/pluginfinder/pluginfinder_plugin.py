import mobase 
from ..shared.shared_plugin import SharedPlugin
from .pluginfinder import PluginFinder

class PluginFinderPlugin(SharedPlugin):

    def __init__(self):
        super().__init__("PluginFinder", "Plugin Finder", mobase.VersionInfo(1,2,6, mobase.ReleaseType.ALPHA))

    def init(self, organiser=mobase.IOrganizer):
        self.pluginfinder = PluginFinder(organiser)
        return super().init(organiser)
    
        