import mobase
from ..core.rootbuilder_plugin import RootBuilderPlugin
from ..modules.rootbuilder_menu import RootBuilderMenu
from ..modules.rootbuilder_update import RootBuilderUpdate
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *

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

    def icon(self):
        return self._icons.linkAltIcon()

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Root Builder Manager.")
    
    def display(self):
        self._dialog.show()
        self._rootBuilderMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), "v" + self.version().displayString(), self.icon())
        self._rootBuilderMenu = RootBuilderMenu(dialog, self._organiser, self._rootBuilder, self._update)
        dialog.addContent(self._rootBuilderMenu)
        return dialog
