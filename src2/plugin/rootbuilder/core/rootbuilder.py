import mobase
from pathlib import Path
from ....common.common_log import CommonLog
from ....common.common_utilities import CommonUtilities
from .rootbuilder_settings import RootBuilderSettings
from ..modules.rootbuilder_strings import RootBuilderStrings
from ..modules.rootbuilder_paths import RootBuilderPaths
from ..modules.rootbuilder_data import RootBuilderData
from ..modules.rootbuilder_cache import RootBuilderCache
from ..modules.rootbuilder_backup import RootBuilderBackup
from ..modules.rootbuilder_builder import RootBuilderBuilder
class RootBuilder():
    """Core Root Builder class that handles all plugin functionality."""

    def __init__(self, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._settings = RootBuilderSettings(self._organiser)
        self._log = CommonLog("RootBuilder", self._organiser, self._settings)
        self._util = CommonUtilities(self._organiser)
        self._strings = RootBuilderStrings("RootBuilder", self._organiser)
        self._paths = RootBuilderPaths("RootBuilder", self._organiser, self._settings, self._strings)
        self._data = RootBuilderData(self._organiser, self._strings, self._paths, self._settings, self._util, self._log)
        self._cache = RootBuilderCache(self._organiser, self._strings, self._paths, self._settings, self._util, self._log)
        self._backup = RootBuilderBackup(self._organiser, self._strings, self._paths, self._settings, self._util, self._log)
        self._builder = RootBuilderBuilder(self._organiser, self._strings, self._paths, self._settings, self._util, self._log)
        super().__init__()

    def build(self):
        """Runs a full build using the current settings."""
        # Generate new build data for what we're about to do.
        hasExistingBuild = self._data.dataFileExists()
        self._log.info("Generating root mod build data.")
        newBuildData = self._data.generateBuildData()

        # Calculate any possible overwrites for if we need to update our backup or cache.
        possibleOverwrites = []
        for fileKey in newBuildData[self._data._copyKey]:
            possibleOverwrites.append(fileKey)
        for fileKey in newBuildData[self._data._linkKey]:
            possibleOverwrites.append(fileKey)

        # Generate a full or partial set of file hashes.
        if self._settings.cache():
            if not self._cache.cacheFileExists():
                self._log.info("No game cache found, generating.")
                fullCache = self._cache.updateCache()
                self._cache.saveCacheFile(fullCache)
        else:
            self._log.info("Cache disabled, only recording potential overwrites.")
            overwriteCache = self._cache.updateOverwriteCache(possibleOverwrites)
            self._cache.saveCacheFile(overwriteCache)

        # Generate a full or partial backup.
        if self._settings.backup():
            self._log.info("Checking for updates to backup files.")
            self._backup.updateBackup()
        else:
            self._log.info("Backup disabled, only storing potential overwrites.")
            self._backup.createPartialBackup(possibleOverwrites)

        # Deploy any files that can go via copy or links.
        self._log.info("Deploying files for Copy mode.")
        self._builder.deployCopy()
        self._log.info("Deploying files for Link mode.")
        self._builder.deployLinks()

        # Update any existing build data or save the new one.
        if hasExistingBuild:
            self._log.info("Previous build data exists, updating.")
            oldBuildData = self._data.loadDataFile()
            newBuildData = self._data.mergeBuildData(oldBuildData, newBuildData)

        self._log.info("Saving build data.")
        self._data.saveDataFile(newBuildData)


    def sync(self):
        """Runs a sync between the game and Mod Organizer."""
        hasExistingBuild = self._data.dataFileExists()
        if hasExistingBuild:
            newData = self._builder.syncFiles()
            self._data.saveDataFile(newData)
            

    def clear(self):
        """Runs a sync and then clears up the game folder."""
        hasExistingBuild = self._data.dataFileExists()
        if hasExistingBuild:
            # Update the files in Mod Organizer if needed.
            self.sync()

            # Delete any deployed files or links
            self._builder.clearFiles()

            # Restore any vanilla files from backup.
            self._backup.restoreBackup()

            # Cleanup any build data if it's not wanted.
            self._data.deleteDataFile()
            if not self._settings.cache():
                self._cache.deleteCacheFile()
            if not self._settings.backup():
                self._backup.deleteBackup()

    def mappings(self):
        """Retrieves mappings for usvfs if applicable."""

    def backup(self):
        """Takes a backup of the current game files."""

    def restore(self):
        """Restores a game from the current backup."""

    def cache(self):
        """Caches the file hashes of a current game."""