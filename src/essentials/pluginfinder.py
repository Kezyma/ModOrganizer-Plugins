from ..pluginfinder.plugins.pluginfinder_browser import PluginFinderBrowser
import mobase

class PluginFinderEssentials(PluginFinderBrowser):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def displayName(self):
        return "Essentials/" + self.baseDisplayName()