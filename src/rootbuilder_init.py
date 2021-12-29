import mobase
from .rootbuilder.plugins.rootbuilder_plugin_mapper import RootBuilderMapperPlugin
from .rootbuilder.plugins.rootbuilder_tool_build import RootBuilderBuildTool
from .rootbuilder.plugins.rootbuilder_tool_clear import RootBuilderClearTool
from .rootbuilder.plugins.rootbuilder_tool_sync import RootBuilderSyncTool
from .rootbuilder.plugins.rootbuilder_tool_manage import RootBuilderManageTool
from .rootbuilder.plugins.rootbuilder_plugin_install import RootBuilderInstallPlugin

def createPlugins():
    return [
        RootBuilderMapperPlugin(),
        RootBuilderBuildTool(),
        RootBuilderClearTool(),
        RootBuilderSyncTool(),
        RootBuilderManageTool(),
        RootBuilderInstallPlugin()
        ]