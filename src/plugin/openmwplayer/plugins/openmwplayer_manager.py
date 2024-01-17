import mobase, threading
from ..core.openmwplayer_plugin import OpenMWPlayerPlugin
from ..modules.openmwplayer_menu import OpenMWPlayerMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *

class OpenMWPlayerManager(OpenMWPlayerPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return OPENMW_ICON

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the OpenMW Player window.")
    
    def display(self):
        self._dialog.show()
        #self._pluginFinderMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), f"v{self.version().displayString()}", self.icon())
        self._openmwPlayerMenu = OpenMWPlayerMenu(dialog, self._organiser, self._openmwPlayer, self._update, self._help)
        dialog.addContent(self._openmwPlayerMenu)
        return dialog