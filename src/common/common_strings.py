import mobase, winreg, os
from functools import cached_property
from pathlib import Path


class CommonStrings:
    """Shared class containing commonly used strings for Mod Organizer plugins."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._plugin = plugin

    @cached_property
    def gameVersion(self) -> str:
        """Gets the currently installed version of the game."""
        version = self._organiser.managedGame().gameVersion()
        if version == "":
            return "unknown"
        return version

    @cached_property
    def gamePath(self) -> str:
        """Gets the path to the current game folder."""
        return self._organiser.managedGame().gameDirectory().path()

    @cached_property
    def gameDataFolder(self) -> str:
        """Gets the name of the Data folder for the current game."""
        return self.gameDataPath.replace(self.gamePath, "")

    @cached_property
    def gameDataPath(self) -> str:
        """Gets the path to the Data folder for the current game."""
        return self._organiser.managedGame().dataDirectory().path()

    @cached_property
    def moPath(self) -> str:
        """Gets the path for Mod Organizer's base folder."""
        return str(Path(__file__).parent.parent.parent.parent)

    @cached_property
    def moLocalePath(self) -> str:
        """Gets the path for Mod Organizer's translations folder."""
        return str(Path(self.moPath) / "translations")

    @cached_property
    def moIniPath(self) -> str:
        return str((Path(self.moInstancePath) / "ModOrganizer.ini").absolute())

    @cached_property
    def moModsPath(self) -> str:
        """Gets the path to Mod Organizer's current mods folder."""
        return self._organiser.modsPath()

    @cached_property
    def moDownloadsPath(self) -> str:
        """Gets the path to Mod Organizer's downloads folder."""
        return self._organiser.downloadsPath()

    @cached_property
    def moExecutablePath(self) -> str:
        """Gets the path to the current ModOrganizer.exe"""
        return str(Path(self.moPath) / "ModOrganizer.exe")

    @cached_property
    def moProfilesPath(self) -> str:
        """Gets the path to the Mod Organizer profiles folder for the current instance."""
        return str(Path(self._organiser.profilePath()).parent)

    @cached_property
    def moProfilePath(self) -> str:
        """Gets the path to the current Mod Organizer profile folder."""
        return self._organiser.profilePath()

    @cached_property
    def moProfileName(self) -> str:
        """Gets the name of the current Mod Organizer profile."""
        return self._organiser.profileName()
    
    @cached_property
    def moInstanceName(self) -> str:
        """Gets the name of the current Mod Organizer instance. Empty if portable."""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\Mod Organizer Team\\Mod Organizer",) as key:
                value = winreg.QueryValueEx(key, "CurrentInstance")
                return str(value[0]).replace("/", "\\")
        except:
            return ""

    @cached_property
    def moInstancesPath(self) -> str:
        """Gets the path to local Mod Organizer instances."""
        return str(Path(os.getenv("LOCALAPPDATA")) / "ModOrganizer")
    
    @cached_property
    def moInstancePath(self) -> str:
        """Gets the path to the current Mod Organizer instance."""
        if self.moInstanceName == "":
            return self.moPath
        return str(Path(self.moInstancesPath) / self.moInstanceName)


    @cached_property
    def moPluginsPath(self) -> str:
        """Gets the path to Mod Organizer's plugins folder."""
        return str(Path(self.moPath) / "plugins")

    @cached_property
    def moOverwritePath(self) -> str:
        """Gets the path to the current overwrite folder."""
        return self._organiser.overwritePath()

    @cached_property
    def pluginDataPath(self) -> str:
        """Gets the path to the data folder for the current plugin."""
        return str(Path(self._organiser.pluginDataPath(), self._plugin).absolute())

    _unsafePathSpaces = [" ", "."]
    _unsafePathStrings = ["<", ">", ":", "|", "*", "\\", "/", "?", "\""]
    def pathSafeString(self, string:str) -> str:
        """Converts a string to one that is safe to use as a file or folder name."""
        for space in self._unsafePathSpaces:
            string = string.replace(space, "_")
        for unsafe in self._unsafePathStrings:
            string = string.replace(unsafe, "")
        return string