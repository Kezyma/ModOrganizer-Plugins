import mobase
from .openmwplayer.plugins.openmwplayer_plugin_launcher import OpenMWPlayerPluginLauncher
from .openmwplayer.plugins.openmwplayer_tool_manage import OpenMWPlayerManageTool
from .openmwplayer.plugins.openmwplayer_tool_export import OpenMWPlayerExportTool

def createPlugins():
    return [
        OpenMWPlayerPluginLauncher(),
        OpenMWPlayerManageTool(),
        OpenMWPlayerExportTool()
        ]