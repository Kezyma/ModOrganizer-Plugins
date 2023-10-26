from .plugin.rootbuilder.plugins.rootbuilder_autobuild import RootBuilderAutobuild
from .plugin.rootbuilder.plugins.rootbuilder_manager import RootBuilderManager

def createPlugins():
    return [
        RootBuilderAutobuild(),
        RootBuilderManager()
    ]