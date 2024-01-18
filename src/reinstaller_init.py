from .plugin.reinstaller.plugins.reinstaller_manager import ReinstallerManager
from .plugin.reinstaller.plugins.reinstaller_quickcreate import ReinstallerQuickCreate
from .plugin.reinstaller.plugins.reinstaller_quickinstall import ReinstallerQuickInstall
from .plugin.reinstaller.plugins.reinstaller_quickdelete import ReinstallerQuickDelete

def createPlugins():
    return [
        ReinstallerManager(),
        ReinstallerQuickCreate(),
        ReinstallerQuickInstall(),
        ReinstallerQuickDelete()
    ]