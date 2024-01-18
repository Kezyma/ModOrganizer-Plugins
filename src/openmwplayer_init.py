from .plugin.openmwplayer.plugins.openmwplayer_manager import OpenMWPlayerManager
from .plugin.openmwplayer.plugins.openmwplayer_launcher import OpenMWPlayerLauncher
from .plugin.openmwplayer.plugins.openmwplayer_quickexport import OpenMWPlayerQuickExport
from .plugin.openmwplayer.plugins.openmwplayer_quickimport import OpenMWPlayerQuickImport
def createPlugins():
    return [
        OpenMWPlayerManager(),
        OpenMWPlayerLauncher(),
        OpenMWPlayerQuickExport(),
        OpenMWPlayerQuickImport()
    ]