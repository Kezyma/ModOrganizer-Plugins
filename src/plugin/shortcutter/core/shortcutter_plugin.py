import mobase
from pathlib import Path
from ....base.base_plugin import BasePlugin
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from .shortcutter import Shortcutter
try:
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt6.QtCore import QCoreApplication

class ShortcutterPlugin(BasePlugin):
    """Base Shortcutter plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("Shortcutter", "Shortcutter", mobase.VersionInfo(2, 0, 0))

    def init(self, organiser:mobase.IOrganizer):
        self._shortcutter = Shortcutter(organiser)
        self._update = CommonUpdate(
            "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/shortcutter.json", 
            "https://www.nexusmods.com/skyrimspecialedition/mods/59827?tab=files", 
            self, self._shortcutter._strings, self._shortcutter._log)
        self._help = CommonHelp(Path(__file__).parent.parent / "data" / "shortcutter_help.html", 
                                "shortcutter", "skyrimspecialedition", "59827", 
                                self._shortcutter._strings, self._shortcutter._log)
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
        