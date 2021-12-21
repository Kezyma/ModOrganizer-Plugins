import mobase
from .creationeer.plugins.creationeer_tool_manage import CreationeerManageTool

def createPlugins():
    return [
        CreationeerManageTool()
        ]