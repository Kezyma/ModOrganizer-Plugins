import mobase
from .openmwplayer.openmwplayer_plugin import OpenMWPlayerPlugin

def createPlugins():
    return [
        OpenMWPlayerPlugin()
        ]