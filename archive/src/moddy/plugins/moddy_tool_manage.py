import mobase

try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

from ..moddy_plugin import ModdyPlugin

class ModdyManageTool(ModdyPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        return res
    
    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []
    
    def icon(self):
        return self.icons.clipIcon()
    
    def name(self):
        return self.baseName() + " Manager Tool"

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Moddy settings manager.")
    
    def display(self):
        qInfo("Display Moddy Settings.")