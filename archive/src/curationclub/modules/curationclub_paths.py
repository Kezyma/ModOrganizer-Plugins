import mobase
from ...shared.shared_paths import SharedPaths
from .curationclub_settings import CurationClubSettings
from pathlib import Path

class CurationClubPaths(SharedPaths):
    """ Curation Club path module. Used to load various paths for the plugin. """

    def __init__(self, settings=CurationClubSettings, organiser=mobase.IOrganizer):
        self.settings = settings
        super().__init__("CurationClub", organiser) 

    _creationsMetaFolder = str()
    def creationsMetaFolder(self):
        if self._creationsMetaFolder == str():
            self._creationsMetaFolder = str(self.gamePath() / "Creations")
        return Path(self._creationsMetaFolder)
    
    def creationsRootFolder(self, modName=str):
        return self.modsPath() / modName / "Root" / "Creations"

    _creationsOverwriteFolder = str()
    def creationsOverwriteFolder(self):
        if self._creationsOverwriteFolder == str():
            self._creationsOverwriteFolder = str(Path(self.organiser.overwritePath()) / "Root" / "Creations")
        return self._creationsOverwriteFolder

    _creationNameCacheFile = str()
    def creationNameCacheFile(self):
        if self._creationNameCacheFile == str():
            self._creationNameCacheFile = self.pluginDataPath() / "creation_cache.json"
        if not Path(self._creationNameCacheFile).exists():
            Path(self._creationNameCacheFile).touch()
        return Path(self._creationNameCacheFile)

    _initialCachePath = str()
    def initialCachePath(self):
        """ Path to the initial directory json to be deployed during install. """
        if self._initialCachePath == str():
            self._initialCachePath = str(Path(__file__).parent.parent / "creation_cache.json")
        return self._initialCachePath