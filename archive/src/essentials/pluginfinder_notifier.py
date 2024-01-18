import mobase

from ..pluginfinder.plugins.pluginfinder_notifier import PluginFinderNotifier


class PluginFinderNotifierEssentials(PluginFinderNotifier):
    def init(self, organiser: mobase.IOrganizer) -> bool:
        return super().init(organiser)
