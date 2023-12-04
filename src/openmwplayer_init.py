from .plugin.openmwplayer.plugins.openmwplayer_manager import OpenMWPlayerManager

def createPlugins():
    return [
        OpenMWPlayerManager()
    ]