try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication
import mobase

class SharedSettings():

    def __init__(self, pluginName = str, organiser = mobase.IOrganizer):
        self.pluginName = pluginName
        self.organiser = organiser
        super().__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def setting(self, settingName=str):
        """ Gets a setting from Mod Organizer. """
        return self.organiser.pluginSetting(self.pluginName, settingName)

    def enabled(self):
        """ Determines whether the plugin is enabled. """
        return self.setting("enabled")