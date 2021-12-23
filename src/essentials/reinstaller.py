from ..reinstaller.plugins.reinstaller_tool_manage import ReinstallerManageTool
import mobase

class ReinstallerEssentials(ReinstallerManageTool):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def displayName(self):
        return "Essentials/" + self.baseDisplayName()