import mobase
from .curationclub.plugins.curationclub_tool_manage import CurationClubManageTool

def createPlugins():
    return [
        CurationClubManageTool()
        ]