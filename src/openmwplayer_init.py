from .plugin.openmwplayer.plugins.openmwplayer_manager import OpenMWPlayerManager
from .plugin.openmwplayer.plugins.openmwplayer_launcher import OpenMWPlayerLauncher

def createPlugins():
    return [
        OpenMWPlayerManager(),
        OpenMWPlayerLauncher()
    ]