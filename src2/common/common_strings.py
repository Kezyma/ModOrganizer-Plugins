import mobase, winreg, os
from pathlib import PurePath, Path


class CommonStrings:
    """Shared class containing commonly used strings for Mod Organizer plugins."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._plugin = plugin

    _gameVersion = str()
    def gameVersion(self) -> str:
        """Gets the currently installed version of the game."""
        if self._gameVersion == str():
            self._gameVersion = self._organiser.managedGame().gameVersion()
            if self._gameVersion == str():
                self._gameVersion = "unknown"
        return self._gameVersion

    _gamePath = str()
    def gamePath(self) -> str:
        """Gets the path to the current game folder."""
        if self._gamePath == str():
            self._gamePath = self._organiser.managedGame().gameDirectory().path()
        return self._gamePath

    _gameDataFolder = str()
    def gameDataFolder(self) -> str:
        """Gets the name of the Data folder for the current game."""
        if self._gameDataFolder == str():
            self._gameDataFolder = PurePath(Path(self.gameDataPath())).name
        return self._gameDataFolder

    _gameDataPath = str()
    def gameDataPath(self) -> str:
        """Gets the path to the Data folder for the current game."""
        if self._gameDataPath == str():
            self._gameDataPath = self._organiser.managedGame().dataDirectory().path()
        return self._gameDataPath

    _moPath = str()
    def moPath(self) -> str:
        """Gets the path for Mod Organizer's base folder."""
        if self._moPath == str():
            self._moPath = str(Path(__file__).parent.parent.parent.parent)
        return self._moPath

    _moIniPath = str()
    def moIniPath(self) -> str:
        if self._moIniPath == str():
            self._moIniPath = str(Path(self.moInstancePath()) / "ModOrganizer.ini")
        return self._moIniPath

    _moModsPath = str()
    def moModsPath(self) -> str:
        """Gets the path to Mod Organizer's current mods folder."""
        if self._moModsPath == str():
            self._moModsPath = self._organiser.modsPath()
        return self._moModsPath

    _moDownloadsPath = str()
    def moDownloadsPath(self) -> str:
        """Gets the path to Mod Organizer's downloads folder."""
        if self._moDownloadsPath == str():
            self._moDownloadsPath = self._organiser.downloadsPath()
        return self._moDownloadsPath

    _moExecutablePath = str()
    def moExecutablePath(self) -> str:
        """Gets the path to the current ModOrganizer.exe"""
        if self._moExecutablePath == str():
            self._moExecutablePath = str(Path(self.moPath()) / "ModOrganizer.exe")
        return self._moExecutablePath

    _moProfilesPath = str()
    def moProfilesPath(self) -> str:
        """Gets the path to the Mod Organizer profiles folder for the current instance."""
        if self._moProfilesPath == str():
            self._moProfilesPath = str(Path(self._organiser.profilePath()).parent)
        return self._moProfilesPath

    def moProfilePath(self) -> str:
        """Gets the path to the current Mod Organizer profile folder."""
        return self._organiser.profilePath()

    def moProfileName(self) -> str:
        """Gets the name of the current Mod Organizer profile."""
        return self._organiser.profileName()
    
    _moInstanceName = str()
    def moInsatanceName(self) -> str:
        """Gets the name of the current Mod Organizer instance. Empty if portable."""
        if self._moInstanceName == str():
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\Mod Organizer Team\\Mod Organizer",) as key:
                    value = winreg.QueryValueEx(key, "CurrentInstance")
                    self._moInstanceName = str(value[0].replace("/", "\\"))
            except:
                self._moInstanceName = str()
        return self._moInstanceName

    _moInstancesPath = str()
    def moInstancesPath(self) -> str:
        """Gets the path to local Mod Organizer instances."""
        if self._moInstancesPath == str():
            self._moInstancesPath = str(Path(os.getenv("LOCALAPPDATA")) / "ModOrganizer")
        return self._moInstancesPath
    
    _moInstancePath = str()
    def moInstancePath(self) -> str:
        """Gets the path to the current Mod Organizer instance."""
        if self._moInstancePath == str():
            currentInstance = self.moInsatanceName()
            if currentInstance == "":
                _moInstancePath = self.moPath()
            else:
                _moInstancePath = str(Path(self.moInstancesPath()) / currentInstance)
        return _moInstancePath

    _moPluginsPath = str()
    def moPluginsPath(self) -> str:
        """Gets the path to Mod Organizer's plugins folder."""
        if self._moPluginsPath == str():
            self._moPluginsPath = str(Path(self.moPath()) / "plugins")
        return self._moPluginsPath

    _moOverwritePath = str()
    def moOverwritePath(self) -> str:
        """Gets the path to the current overwrite folder."""
        if self._moOverwritePath == str():
            self._moOverwritePath = self.organiser.overwritePath()
        return self._moOverwritePath

    _pluginDataPath = str
    def pluginDataPath(self) -> str:
        """Gets the path to the data folder for the current plugin."""
        if self._pluginDataPath == str():
            self._pluginDataPath = str(Path(self._organiser.pluginDataPath()) / self._plugin)
        return self._pluginDataPath
    
    _unsafePathSpaces = [" ", "."]
    _unsafePathStrings = ["<", ">", ":", "|", "*", "\\", "/", "?", "\""]
    def pathSafeString(self, string:str) -> str:
        """Converts a string to one that is safe to use as a file or folder name."""
        for space in self._unsafePathSpaces:
            string = string.replace(space, "_")
        for unsafe in self._unsafePathStrings:
            string = string.replace(unsafe, "")
        return string