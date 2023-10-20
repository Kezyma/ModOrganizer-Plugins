import mobase
from .openmwplayer.plugins.openmwplayer_plugin_launcher import OpenMWPlayerPluginLauncher
from .openmwplayer.plugins.openmwplayer_tool_manage import OpenMWPlayerManageTool
from .openmwplayer.plugins.openmwplayer_tool_export import OpenMWPlayerExportTool
from .openmwplayer.plugins.openmwplayer_tool_import import OpenMWPlayerImportTool

def createPlugins():
    return [
        OpenMWPlayerPluginLauncher(),
        OpenMWPlayerManageTool(),
        OpenMWPlayerExportTool(),
        OpenMWPlayerImportTool()
        ]