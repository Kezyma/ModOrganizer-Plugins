try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication
    
import mobase

class BaseSettings():
    """ Base class for settings modules to inherit from. Contains settings shared across plugins. """

    def __init__(self, pluginName = str, organiser = mobase.IOrganizer):
        self._pluginName = pluginName
        self._organiser = organiser
        super().__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def setting(self, settingName=str):
        """ Gets a setting from Mod Organizer. """
        return self._organiser.pluginSetting(self._pluginName, settingName)

    def enabled(self):
        """ Determines whether the plugin is enabled. """
        return self.setting("enabled")
    
    def loglevel(self):
        """ Determines whether the plugin is in debug mode. """
        return self.setting("loglevel")