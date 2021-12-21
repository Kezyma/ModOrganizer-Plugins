from ..creationeer_plugin import CreationeerPlugin
import mobase
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class CreationeerManageTool(CreationeerPlugin, mobase.IPluginTool):
    
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.menuIcon()
        
    def description(self):
        return self.__tr("Sorts CC content.")

    def display(self):
        self.creationeer.sort()
        
        
        
        
        
        
        