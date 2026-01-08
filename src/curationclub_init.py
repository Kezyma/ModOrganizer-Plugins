from .plugin.curationclub.plugins.curationclub_manager import CurationClubManager


def createPlugins():
    return [
        CurationClubManager()
    ]
