import mobase, os, winreg, glob
from pathlib import Path, PurePath
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class SharedPaths():

    def __init__(self, pluginName = str, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.pluginName = pluginName
        super().__init__()
        
    _version = str()
    def gameVersion(self):
        """ Gets the current game version string. """
        if self._version == str():
            self._version = self.organiser.managedGame().gameVersion()
        if self._version == str():
            return "Unknown"
        return self._version

    _gamePath = str()
    def gamePath(self):
        """ Gets the path to the current game folder. """
        if self._gamePath == str():
            self._gamePath = self.organiser.managedGame().gameDirectory().path()
        return Path(self._gamePath)

    _modsPath = str()
    def modsPath(self):
        """ Gets the path to the current mod folder. """
        if self._modsPath == str():
            self._modsPath = self.organiser.modsPath()
        return Path(self._modsPath)

    _gameDataDir = str()
    def gameDataDir(self):
        """ Gets the name of the data directory for the current game. """
        if self._gameDataDir == str():
            self._gameDataDir = PurePath(Path(self.organiser.managedGame().dataDirectory().path())).name
        return self._gameDataDir

    _downloadsPath = str()
    def downloadsPath(self):
        """ Gets the path to the current downloads folder. """
        if self._downloadsPath == str():
            self._downloadsPath = self.organiser.downloadsPath()
        return Path(self._downloadsPath)

    _pluginDataPath = str()
    def pluginDataPath(self):
        """ Gets the path to the data folder for this plugin. """
        if self._pluginDataPath == str():
            self._pluginDataPath = Path(self.organiser.pluginDataPath()) / self.pluginName
        if not Path(self._pluginDataPath).exists():
            os.makedirs(self._pluginDataPath)
        return Path(self._pluginDataPath)

    _safeGamePathName = str()
    def safeGamePathName(self):
        """ Gets a file safe string representing the current game install. """
        if self._safeGamePathName == str():
            self._safeGamePathName = self.safePathName(self.gamePath())
        return self._safeGamePathName

    _modOrganizerPath = str()
    def modOrganizerPath(self):
        """ Gets the path for Mod Organizer's base folder. """
        if self._modOrganizerPath == str():
            self._modOrganizerPath = Path(__file__).parent.parent.parent.parent
        return Path(self._modOrganizerPath)

    _modOrganizerExePath = str()
    def modOrganizerExePath(self):
        """ Gets the path to the current ModOrganizer.exe """
        if self._modOrganizerExePath == str():
            self._modOrganizerExePath = str(self.modOrganizerPath() / "ModOrganizer.exe")
        return Path(self._modOrganizerExePath)

    _modOrganizerProfilesPath = str()
    def modOrganizerProfilesPath(self):
        """ Gets the path to Mod Organizer's profiles folder. """
        if self._modOrganizerProfilesPath == str():
            self._modOrganizerProfilesPath = str(Path(self.organiser.profilePath()).parent)
        return Path(self._modOrganizerProfilesPath)

    _modOrganizerInstancesPath = str()
    def modOrganizerInstancesPath(self):
        if self._modOrganizerInstancesPath == str():
            self._modOrganizerInstancesPath = Path(os.getenv("LOCALAPPDATA")) / "ModOrganizer"
        return Path(self._modOrganizerInstancesPath)

    def currentInstanceName(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Mod Organizer Team\\Mod Organizer") as key:
                value = winreg.QueryValueEx(key, "CurrentInstance")
                result = str(value[0].replace("/", "\\"))
                return result
        except:
            return ""

    def modOrganizerIniPath(self):
        if self.currentInstanceName() == "":
            return self.modOrganizerPath() / "ModOrganizer.ini"
        else:
            return self.modOrganizerInstancesPath() / self.currentInstanceName() / "ModOrganizer.ini"

    def modOrganizerApps(self):
        return self.modOrganizerAppPaths().keys()

    def modOrganizerAppPaths(self):
        paths = {}
        names = {}
        with open(self.modOrganizerIniPath()) as ini:
            for line in ini:
                txt = line.rstrip()
                parts = txt.split("\\")
                if len(parts) > 1:
                    appId = parts[0]
                    part = parts[1].split("=")
                    if part[0] == "title":
                        names[appId] = part[1]
                    if part[0] == "binary":
                        paths[appId] = part[1]
        res = {}
        for appId in names.keys():
            res[names[appId]] = paths[appId]
        return res

    def modOrganizerProfile(self):
        """ Gets the name of the current profile. """
        return self.organiser.profileName()
    
    def gameRelativePath(self, path):
        """ Gets the part of a path relative to the current game folder. """
        return Path(str(os.path.abspath(Path(path))).replace(str(os.path.abspath(self.gamePath())), "")[1:])

    def relativePath(self, basePath, searchPath):
        return Path(str(os.path.abspath(Path(searchPath))).replace(str(os.path.abspath(str(basePath))), "")[1:])

    def safePathName(self, path):
        """ Gets a file safe string representing a specific path. """
        return self.fileSafeName("_".join(os.path.normpath(path).split(os.path.sep)))

    def fileSafeName(self, string=str):
        return string.replace(" ", "_").replace(".", "_").replace("<", "").replace(">", "").replace(":", "").replace("|", "").replace("*", "").replace("\\", "").replace("/", "").replace("?", "").replace("\"", "")

    def safeVersionName(self, version):
        """ Gets a file safe string representing a specific game version. """
        return self.fileSafeName(version)

    def sharedPath(self, basePath, childPath):
        """ Determines whether one path is a child of another path. Supports * wildcard. """
        if "*" in str(basePath):
            result = False
            for path in glob.glob(str(basePath)):
                if self.sharedPath(path, childPath):
                    result = True
            return result
        try:
            if os.path.commonpath([os.path.abspath(basePath), os.path.abspath(childPath)]) == os.path.commonpath([os.path.abspath(basePath)]):
                return True
        except:
            return False
        return False

    def fileExists(self, filePath):
        """ Determines whether a file already exists. Supports * wildcard. """
        if "*" in str(filePath):
            #("Searching for " + str(filePath))
            for path in glob.glob(str(filePath)):
                #qInfo("Found " + path)
                if path != "":
                    return True
        elif Path(filePath).exists():
            return True
        return False