from .plugin.pluginfinder.plugins.pluginfinder_manager import PluginFinderManager
from .plugin.pluginfinder.plugins.pluginfinder_updater import PluginFinderUpdater
from .plugin.pluginfinder.plugins.pluginfinder_installer import PluginFinderInstaller

def createPlugins():
    return [
        PluginFinderManager(),
        PluginFinderUpdater(),
        PluginFinderInstaller()
    ]