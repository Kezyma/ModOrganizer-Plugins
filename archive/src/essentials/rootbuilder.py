from ..rootbuilder.plugins.rootbuilder_tool_manage import RootBuilderManageTool
import mobase

class RootBuilderEssentials(RootBuilderManageTool):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def displayName(self):
        return "Essentials/" + self.baseDisplayName()