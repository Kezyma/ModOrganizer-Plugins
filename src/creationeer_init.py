import mobase
from .creationeer.plugins.creationeer_tool_manage import CurationClubManageTool

def createPlugins():
    return [
        CurationClubManageTool()
        ]