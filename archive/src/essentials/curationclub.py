from ..curationclub.plugins.curationclub_tool_manage import CurationClubManageTool
import mobase

class CurationClubEssentials(CurationClubManageTool):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def displayName(self):
        return "Essentials/" + self.baseDisplayName()