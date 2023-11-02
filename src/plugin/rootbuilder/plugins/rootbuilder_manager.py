import mobase
from ..core.rootbuilder_plugin import RootBuilderPlugin
from ..modules.rootbuilder_menu import RootBuilderMenu
from ..modules.rootbuilder_update import RootBuilderUpdate
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import LINK_ALT_ICON

class RootBuilderManager(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._update = RootBuilderUpdate(self._organiser, self, self._rootBuilder._strings, self._rootBuilder._util, self._rootBuilder._log)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self._pluginName

    def settings(self):
        return []

    def icon(self):
        return LINK_ALT_ICON

    def name(self):
        return f"{self.baseName()} Manager Tool"

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Root Builder Manager.")
    
    def display(self):
        self._dialog.show()
        self._rootBuilderMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), f"v{self.version().displayString()}", self.icon())
        self._rootBuilderMenu = RootBuilderMenu(dialog, self._organiser, self._rootBuilder, self._update)
        dialog.addContent(self._rootBuilderMenu)
        return dialog
