import mobase, winreg, os
from pathlib import Path


class CommonStrings:
    """Shared class containing commonly used strings for Mod Organizer plugins."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._plugin = plugin

    _gameVersion = ""
    def gameVersion(self) -> str:
        """Gets the currently installed version of the game."""
        if self._gameVersion == "":
            self._gameVersion = self._organiser.managedGame().gameVersion()
            if self._gameVersion == "":
                self._gameVersion = "unknown"
        return self._gameVersion

    _gamePath = ""
    def gamePath(self) -> str:
        """Gets the path to the current game folder."""
        if self._gamePath == "":
            self._gamePath = self._organiser.managedGame().gameDirectory().path()
        return self._gamePath

    _gameDataFolder = ""
    def gameDataFolder(self) -> str:
        """Gets the name of the Data folder for the current game."""
        if self._gameDataFolder == "":
            gamePath = self.gamePath()
            gameDataPath = self.gameDataPath()
            self._gameDataFolder = gameDataPath.replace(gamePath, "")
        return self._gameDataFolder

    _gameDataPath = ""
    def gameDataPath(self) -> str:
        """Gets the path to the Data folder for the current game."""
        if self._gameDataPath == "":
            self._gameDataPath = self._organiser.managedGame().dataDirectory().path()
        return self._gameDataPath

    _moPath = ""
    def moPath(self) -> str:
        """Gets the path for Mod Organizer's base folder."""
        if self._moPath == "":
            self._moPath = str(Path(__file__).parent.parent.parent.parent)
        return self._moPath

    _moIniPath = ""
    def moIniPath(self) -> str:
        if self._moIniPath == "":
            moIniPath = Path(self.moInstancePath() / "ModOrganizer.ini")
            self._moIniPath = str(moIniPath.absolute())
        return self._moIniPath

    _moModsPath = ""
    def moModsPath(self) -> str:
        """Gets the path to Mod Organizer's current mods folder."""
        if self._moModsPath == "":
            self._moModsPath = self._organiser.modsPath()
        return self._moModsPath

    _moDownloadsPath = ""
    def moDownloadsPath(self) -> str:
        """Gets the path to Mod Organizer's downloads folder."""
        if self._moDownloadsPath == "":
            self._moDownloadsPath = self._organiser.downloadsPath()
        return self._moDownloadsPath

    _moExecutablePath = ""
    def moExecutablePath(self) -> str:
        """Gets the path to the current ModOrganizer.exe"""
        if self._moExecutablePath == "":
            self._moExecutablePath = str(Path(self.moPath()) / "ModOrganizer.exe")
        return self._moExecutablePath

    _moProfilesPath = ""
    def moProfilesPath(self) -> str:
        """Gets the path to the Mod Organizer profiles folder for the current instance."""
        if self._moProfilesPath == "":
            self._moProfilesPath = str(Path(self._organiser.profilePath()).parent)
        return self._moProfilesPath

    def moProfilePath(self) -> str:
        """Gets the path to the current Mod Organizer profile folder."""
        return self._organiser.profilePath()

    def moProfileName(self) -> str:
        """Gets the name of the current Mod Organizer profile."""
        return self._organiser.profileName()
    
    _moInstanceName = ""
    def moInsatanceName(self) -> str:
        """Gets the name of the current Mod Organizer instance. Empty if portable."""
        if self._moInstanceName == "":
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\Mod Organizer Team\\Mod Organizer",) as key:
                    value = winreg.QueryValueEx(key, "CurrentInstance")
                    self._moInstanceName = str(value[0]).replace("/", "\\")
            except:
                self._moInstanceName = ""
        return self._moInstanceName

    _moInstancesPath = ""
    def moInstancesPath(self) -> str:
        """Gets the path to local Mod Organizer instances."""
        if self._moInstancesPath == "":
            self._moInstancesPath = str(Path(os.getenv("LOCALAPPDATA")) / "ModOrganizer")
        return self._moInstancesPath
    
    _moInstancePath = ""
    def moInstancePath(self) -> str:
        """Gets the path to the current Mod Organizer instance."""
        if self._moInstancePath == "":
            currentInstance = self.moInsatanceName()
            if currentInstance == "":
                _moInstancePath = self.moPath()
            else:
                _moInstancePath = str(Path(self.moInstancesPath()) / currentInstance)
        return _moInstancePath

    _moPluginsPath = ""
    def moPluginsPath(self) -> str:
        """Gets the path to Mod Organizer's plugins folder."""
        if self._moPluginsPath == "":
            self._moPluginsPath = str(Path(self.moPath()) / "plugins")
        return self._moPluginsPath

    _moOverwritePath = ""
    def moOverwritePath(self) -> str:
        """Gets the path to the current overwrite folder."""
        if self._moOverwritePath == "":
            self._moOverwritePath = self._organiser.overwritePath()
        return self._moOverwritePath

    _pluginDataPath = ""
    def pluginDataPath(self) -> str:
        """Gets the path to the data folder for the current plugin."""
        if self._pluginDataPath == "":
            pluginDataPath = Path(self._organiser.pluginDataPath(), self._plugin)
            self._pluginDataPath = str(pluginDataPath.absolute())
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