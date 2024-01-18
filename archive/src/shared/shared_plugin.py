import mobase
try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication
from .shared_icons import SharedIcons
from .shared_settings import SharedSettings

class SharedPlugin():
    
    def __init__(self, pluginName = str, displayName = str, version = mobase.VersionInfo):
        self.pluginName = pluginName
        self.baseDisplayNameVal = displayName
        self.versionInfo = version
        super().__init__()

    def init(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.baseSettings = SharedSettings(self.pluginName, self.organiser)
        self.icons = SharedIcons()
        return True

    def version(self):
        return self.versionInfo

    def isActive(self):
        return self.baseSettings.enabled()

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def tr(self, trstr):
        return self.__tr(trstr)

    def icon(self):
        return self.icons.menuIcon()

    def author(self):
        return "Kezyma"

    def baseName(self):
        return self.pluginName

    def baseDisplayName(self):
        return self.baseDisplayNameVal

    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Plugin description. Overwrite me.")

    def tooltip(self):
        return self.description()

    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("enabled",self.__tr("Enables " + self.pluginName),True)
            ]