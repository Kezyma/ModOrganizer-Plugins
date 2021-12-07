import mobase, os
from pathlib import Path, PurePath

class SharedPaths():

    def __init__(self, pluginName = str, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.pluginName = pluginName
        super().__init__()

    def gameVersion(self):
        """ Gets the current game version string. """
        return self.organiser.managedGame().gameVersion()

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

    def gameRelativePath(self, path):
        """ Gets the part of a path relative to the current game folder. """
        return Path(str(os.path.abspath(Path(path))).replace(str(os.path.abspath(self.gamePath())), "")[1:])

    def safePathName(self, path):
        """ Gets a file safe string representing a specific path. """
        return "_".join(os.path.normpath(path).split(os.path.sep)).replace(":", "").replace(" ", "_")

    def safeVersionName(self, version):
        """ Gets a file safe string representing a specific game version. """
        return version.replace(".", "_").replace(":", "_")

    def sharedPath(self, basePath, childPath):
        """ Determines whether one path is a child of another path. """
        try:
            if os.path.commonpath([os.path.abspath(basePath), os.path.abspath(childPath)]) == os.path.commonpath([os.path.abspath(basePath)]):
                return True
        except:
            return False
        return False
