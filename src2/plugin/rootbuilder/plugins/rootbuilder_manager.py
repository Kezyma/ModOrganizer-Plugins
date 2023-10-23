import mobase
from ..core.rootbuilder_plugin import RootBuilderPlugin
from ..core.rootbuilder_menu import RootBuilderMenu
from ....base.base_dialog import BaseDialog
try:
    from PyQt5.QtCore import QCoreApplication
    from PyQt5 import QtWidgets
except:
    from PyQt6.QtCore import QCoreApplication
    from PyQt6 import QtWidgets

class RootBuilderManager(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self._pluginName

    def settings(self):
        return []

    def icon(self):
        return self._icons.linkAltIcon()

    def name(self):
        return self.baseName() + " Manager Tool"

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Root Builder Manager.")
    
    def display(self):
        self._dialog.show()
        self._rootBuilderMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), "v" + self.version().displayString(), self.icon())
        self._rootBuilderMenu = RootBuilderMenu(dialog, self._organiser, self._rootBuilder)
        dialog.addContent(self._rootBuilderMenu)
        return dialog
