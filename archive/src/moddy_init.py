import mobase
from .moddy.plugins.moddy_plugin_checker import ModdyCheckerPlugin
from .moddy.plugins.moddy_tool_manage import ModdyManageTool

def createPlugins():
    return [
        ModdyCheckerPlugin(),
        ModdyManageTool()
        ]