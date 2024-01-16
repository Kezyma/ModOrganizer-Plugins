import mobase
from ..core.shortcutter_plugin import ShortcutterPlugin
from ..modules.shortcutter_menu import ShortcutterMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import LINK_ICON

class ShortcutterManager(ShortcutterPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return LINK_ICON

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Shortcutter menu.")
    
    def display(self):
        self._shortcutterMenu.rebind()
        self._dialog.show()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), f"v{self.version().displayString()}", self.icon())
        self._shortcutterMenu = ShortcutterMenu(dialog, self._organiser, self._shortcutter, self._update, self._help)
        dialog.addContent(self._shortcutterMenu)
        return dialog
