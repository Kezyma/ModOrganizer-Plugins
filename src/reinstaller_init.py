import mobase
from .reinstaller.plugins.reinstaller_tool_create import ReinstallerCreateTool
from .reinstaller.plugins.reinstaller_tool_install import ReinstallerInstallTool
from .reinstaller.plugins.reinstaller_tool_delete import ReinstallerDeleteTool
from .reinstaller.plugins.reinstaller_tool_manage import ReinstallerManageTool

def createPlugins():
    return [
        ReinstallerCreateTool(),
        ReinstallerInstallTool(),
        ReinstallerDeleteTool(),
        ReinstallerManageTool()
        ]