import mobase
from .pluginfinder.plugins.pluginfinder_tool_manage import PluginFinderManageTool

def createPlugins():
    return [
        PluginFinderManageTool()
        ]