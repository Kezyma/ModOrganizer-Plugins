"""Curation Club settings management."""

import mobase
from ....base.base_settings import BaseSettings


class CurationClubSettings(BaseSettings):
    """Settings manager for Curation Club plugin."""

    def __init__(self, organiser: mobase.IOrganizer):
        super().__init__("CurationClub", organiser)

    def groupmode(self) -> str:
        """
        Returns the grouping mode for creations.
        'separate' - Each creation in its own mod
        'single' - All creations in one mod
        """
        return str(self.setting("groupmode"))

    def updateGroupmode(self, value: str):
        """Updates the grouping mode setting."""
        self.updateSetting("groupmode", value)

    def nameformat(self) -> str:
        """Returns the name format template for individual mods."""
        return str(self.setting("nameformat"))

    def updateNameformat(self, value: str):
        """Updates the name format template."""
        self.updateSetting("nameformat", value)

    def combinedname(self) -> str:
        """Returns the name for the combined mod (when groupmode is 'single')."""
        return str(self.setting("combinedname"))

    def updateCombinedname(self, value: str):
        """Updates the combined mod name."""
        self.updateSetting("combinedname", value)
