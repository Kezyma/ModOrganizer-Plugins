import mobase
from .pluginfinder.plugins.pluginfinder_browser import PluginFinderBrowser

def createPlugins():
    return [
        PluginFinderBrowser()
        ]

