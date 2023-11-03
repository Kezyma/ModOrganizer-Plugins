from .plugin.pluginfinder.plugins.pluginfinder_manager import PluginFinderManager

def createPlugins():
    return [
        PluginFinderManager()
    ]