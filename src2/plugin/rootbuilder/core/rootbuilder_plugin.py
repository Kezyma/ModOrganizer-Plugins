import mobase
from ....base.base_plugin import BasePlugin
from ....common.common_ui import CommonUI
from .rootbuilder import RootBuilder
try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication

class RootBuilderPlugin(BasePlugin):
    """Base Root Builder plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("RootBuilder", "Root Builder", mobase.VersionInfo(5, 0, 0, mobase.ReleaseType.FINAL))

    def init(self, organiser=mobase.IOrganizer):
        self._rootBuilder = RootBuilder(organiser)
        self._ui = CommonUI()
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting("cache",self.__tr("Enables caching of base game files on first run."), True),
            mobase.PluginSetting("backup",self.__tr("Enables full backup of base game files on first run."), True),
            mobase.PluginSetting("autobuild",self.__tr("Enables automatic build and clear on running an application through Mod Organizer."), True),
            mobase.PluginSetting("redirect", self.__tr("Enables automatic redirection of exe files being launched from a mod folder to their respective game folder equivalent."), True),
            mobase.PluginSetting("installer", self.__tr("Enables an installer plugin to automatically install root mods when detected."), False),
            mobase.PluginSetting("priority", self.__tr("The priority of the installer module for installing root mods."), 110),
            mobase.PluginSetting("exclusions",self.__tr("List of files and folders to exclude from RootBuilder."), "Saves,Morrowind.ini"),
            mobase.PluginSetting("copyfiles",self.__tr("Determines the files that should be copied."), "**"),
            mobase.PluginSetting("linkfiles", self.__tr("Determines the files that should be linked."), ""),
            mobase.PluginSetting("usvfsfiles",self.__tr("Determines the files that should be mapped with usvfs"), ""),
            mobase.PluginSetting("copypriority",self.__tr("Priority order for determining when to copy files. Lower is better."), 1),
            mobase.PluginSetting("linkpriority",self.__tr("Priority order for determining when to link files. Lower is better."), 2),
            mobase.PluginSetting("usvfspriority",self.__tr("Priority order for determining when to usvfs map files. Lower is better."), 3),
            mobase.PluginSetting("enabled",self.__tr("Enables " + self._pluginName), True),
            mobase.PluginSetting("loglevel", self.__tr("Controls the logging for " + self._pluginName), 1)
            ]
        for setting in customSettings:
            baseSettings.append(setting)
        return customSettings
        