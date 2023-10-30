from .plugin.rootbuilder.plugins.rootbuilder_autobuild import RootBuilderAutobuild
from .plugin.rootbuilder.plugins.rootbuilder_manager import RootBuilderManager
from .plugin.rootbuilder.plugins.rootbuilder_installer import RootBuilderInstaller

def createPlugins():
    return [
        RootBuilderAutobuild(),
        RootBuilderManager(),
        RootBuilderInstaller()
    ]