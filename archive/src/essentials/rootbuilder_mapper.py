from ..rootbuilder.plugins.rootbuilder_plugin_mapper import RootBuilderMapperPlugin
import mobase

class RootBuilderMapperEssentials(RootBuilderMapperPlugin):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)