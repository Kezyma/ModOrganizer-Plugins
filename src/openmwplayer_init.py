import mobase
from .openmwplayer.plugins.openmwplayer_plugin_launcher import OpenMWPlayerPluginLauncher
from .openmwplayer.plugins.openmwplayer_tool_manage import OpenMWPlayerManageTool

def createPlugins():
    return [
        OpenMWPlayerPluginLauncher(),
        OpenMWPlayerManageTool()
        ]