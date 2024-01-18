from .plugin.rootbuilder.plugins.rootbuilder_autobuild import RootBuilderAutobuild
from .plugin.rootbuilder.plugins.rootbuilder_manager import RootBuilderManager
from .plugin.rootbuilder.plugins.rootbuilder_installer import RootBuilderInstaller
from .plugin.rootbuilder.plugins.rootbuilder_quickbuild import RootBuilderQuickBuild
from .plugin.rootbuilder.plugins.rootbuilder_quicksync import RootBuilderQuickSync
from .plugin.rootbuilder.plugins.rootbuilder_quickclear import RootBuilderQuickClear

def createPlugins():
    return [
        RootBuilderAutobuild(),
        RootBuilderManager(),
        RootBuilderInstaller(),
        RootBuilderQuickBuild(),
        RootBuilderQuickSync(),
        RootBuilderQuickClear()
    ]