from typing import List

import mobase

from .pluginfinder.plugins.pluginfinder_browser import PluginFinderBrowser
from .pluginfinder.plugins.pluginfinder_notifier import PluginFinderNotifier


def createPlugins() -> List[mobase.IPlugin]:
    return [
        PluginFinderBrowser(),
        PluginFinderNotifier(),
    ]
