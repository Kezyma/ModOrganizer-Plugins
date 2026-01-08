"""Curation Club base plugin class."""

import mobase
from ....base.base_plugin import BasePlugin
from .curationclub_settings import CurationClubSettings


class CurationClubPlugin(BasePlugin):
    """Base plugin class for Curation Club plugins."""

    def __init__(self):
        super().__init__("CurationClub", "Curation Club", mobase.VersionInfo(1, 0, 0))

    def init(self, organiser: mobase.IOrganizer) -> bool:
        res = super().init(organiser)
        self._settings = CurationClubSettings(self._organiser)
        return res

    def settings(self):
        """Returns the list of plugin settings."""
        return [
            mobase.PluginSetting("enabled", "Enable this plugin.", True),
            mobase.PluginSetting("loglevel", "Logging level (debug, info, warning, critical).", "info"),
            mobase.PluginSetting("groupmode", "Grouping mode: 'separate' for individual mods, 'single' for combined.", "separate"),
            mobase.PluginSetting("nameformat", "Name format for individual mods. Use {NAME} and {ID} as placeholders.", "Creation Club - {NAME}"),
            mobase.PluginSetting("combinedname", "Name for combined mod when using 'single' mode.", "Creation Club Content"),
        ]

    def author(self) -> str:
        return "Kezyma"

    def description(self) -> str:
        return self.tr("Manages Creation Club content by organizing it into MO2 mods.")
