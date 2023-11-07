import mobase, threading
from ..core.pluginfinder_plugin import PluginFinderPlugin
from ..modules.pluginfinder_menu import PluginFinderMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *

class PluginFinderManager(PluginFinderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._organiser.onUserInterfaceInitialized(lambda window: self.initialSetup())
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return PLUGIN_ICON

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Plugin Finder window.")
    
    def display(self):
        self._dialog.show()
        self._pluginFinderMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), f"v{self.version().displayString()}", self.icon())
        dialog.rejected.connect(self._pluginFinder._install.reloadData)
        self._pluginFinderMenu = PluginFinderMenu(dialog, self._organiser, self._pluginFinder)
        dialog.addContent(self._pluginFinderMenu)
        return dialog

    def initialSetup(self):
        self._pluginFinder._directory.initialDeploy()
        nt = threading.Thread(target=self._pluginFinder._install.detectCurrentPlugins)
        nt.start()