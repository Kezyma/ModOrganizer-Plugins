import mobase
from ..core.profilesync_plugin import ProfileSyncPlugin
from ..modules.profilesync_menu import ProfileSyncMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *

class ProfileSyncManager(ProfileSyncPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    #def master(self):
    #    return self._pluginName

    #def settings(self):
    #    return []

    def icon(self):
        return self._icons.syncIcon()

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Manage Profile Sync groups.")
    
    def display(self):
        self._dialog.show()
        #self._profileSyncMenu.rebind()

    def getDialog(self) -> QtWidgets.QDialog:
        dialog = BaseDialog(self.displayName(), "v" + self.version().displayString(), self.icon())
        self._profileSyncMenu = ProfileSyncMenu(dialog, self._organiser, self._profileSync)
        dialog.addContent(self._profileSyncMenu)
        return dialog
