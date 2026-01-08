"""Curation Club string constants and paths."""

import mobase
import os
from pathlib import Path


class CurationClubStrings:
    """String constants and path utilities for Curation Club."""

    def __init__(self, plugin: str, organiser: mobase.IOrganizer):
        self._organiser = organiser
        self._plugin = plugin

    @property
    def pluginDataPath(self) -> str:
        """Returns the plugin data folder path."""
        return str(Path(self._organiser.basePath()) / self._plugin)

    @property
    def creationsDatabasePath(self) -> str:
        """Returns the path to the cached creations database."""
        return str(Path(self.pluginDataPath) / "creations_database.json")

    @property
    def manualCreationsPath(self) -> str:
        """Returns the path to manually added creations."""
        return str(Path(self.pluginDataPath) / "manual_creations.json")

    @property
    def curationStatePath(self) -> str:
        """Returns the path to the curation state file."""
        return str(Path(self.pluginDataPath) / "curation_state.json")

    @property
    def defaultDatabasePath(self) -> str:
        """Returns the path to the bundled default database."""
        return str(Path(__file__).parent.parent / "data" / "curationclub_creations.json")

    @property
    def gameDataPath(self) -> str:
        """Returns the game's Data folder path."""
        game = self._organiser.managedGame()
        return str(Path(game.dataDirectory().absolutePath()))

    @property
    def gamePath(self) -> str:
        """Returns the game's root folder path."""
        game = self._organiser.managedGame()
        return str(Path(game.gameDirectory().absolutePath()))

    @property
    def moModsPath(self) -> str:
        """Returns the MO2 mods folder path."""
        return str(Path(self._organiser.modsPath()))

    @property
    def moProfilesPath(self) -> str:
        """Returns the MO2 profiles folder path."""
        return str(Path(self._organiser.basePath()) / "profiles")

    @property
    def moExecutablePath(self) -> str:
        """Returns the MO2 executable path."""
        return str(Path(self._organiser.basePath()) / "ModOrganizer.exe")

    def ensureDataFolder(self):
        """Ensures the plugin data folder exists."""
        dataPath = Path(self.pluginDataPath)
        dataPath.mkdir(parents=True, exist_ok=True)

    def initializeDatabase(self):
        """Copies the default database if none exists."""
        self.ensureDataFolder()
        dbPath = Path(self.creationsDatabasePath)
        if not dbPath.exists():
            defaultPath = Path(self.defaultDatabasePath)
            if defaultPath.exists():
                import shutil
                shutil.copy(str(defaultPath), str(dbPath))
