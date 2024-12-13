import mobase
from pathlib import Path
from ....base.base_plugin import BasePlugin
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from .reinstaller import Reinstaller, ReinstallerNoCopy

try:
    from PyQt5.QtCore import QCoreApplication
except ImportError:
    from PyQt6.QtCore import QCoreApplication


class ReinstallerPlugin(BasePlugin):
    """Base Reinstaller plugin, to be inherited by all other plugins."""

    def __init__(self):
        super().__init__("Reinstaller", "Reinstaller", mobase.VersionInfo(2, 0, 1))

    def init(self, organiser: mobase.IOrganizer):
        if organiser.pluginSetting(self.name(), "copy_installers"):
            self._reinstaller = Reinstaller(organiser)
        else:
            self._reinstaller = ReinstallerNoCopy(organiser)

        self._update = CommonUpdate(
            "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/reinstaller.json",
            "https://www.nexusmods.com/skyrimspecialedition/mods/59292?tab=files",
            self,
            self._reinstaller._strings,
            self._reinstaller._log,
        )
        self._help = CommonHelp(
            Path(__file__).parent.parent / "data" / "reinstaller_help.html",
            "reinstaller",
            "skyrimspecialedition",
            "59292",
            self._reinstaller._strings,
            self._reinstaller._log,
        )
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def settings(self):
        """Current list of game settings for Mod Organizer."""
        baseSettings = super().settings()
        customSettings = [
            mobase.PluginSetting(
                "copy_installers",
                "Backup installers out of download folder",
                True,
            ),
        ]
        for setting in customSettings:
            baseSettings.append(setting)
        return baseSettings
