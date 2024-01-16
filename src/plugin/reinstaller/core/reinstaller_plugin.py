import mobase
from ....base.base_plugin import BasePlugin
from ....common.common_update import CommonUpdate
from .reinstaller import Reinstaller
try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication

class ReinstallerPlugin(BasePlugin):
    """Base Reinstaller plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("Reinstaller", "Reinstaller", mobase.VersionInfo(2, 0, 0))

    def init(self, organiser:mobase.IOrganizer):
        self._reinstaller = Reinstaller(organiser)
        self._update = CommonUpdate(
            "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/reinstaller.json", 
            "https://www.nexusmods.com/skyrimspecialedition/mods/59292?tab=files", 
            self, self._reinstaller._strings, self._reinstaller._log)
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)
    
    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        baseSettings = super().settings()
        customSettings = []
        for setting in customSettings:
            baseSettings.append(setting)
        return baseSettings
        