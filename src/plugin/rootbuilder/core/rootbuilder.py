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
from ..modules.rootbuilder_export import RootBuilderExport
from ..modules.rootbuilder_legacy import RootBuilderLegacy
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
        self._backup = RootBuilderBackup(self._organiser, self._strings, self._paths, self._settings, self._cache, self._util, self._log)
        self._builder = RootBuilderBuilder(self._organiser, self._strings, self._paths, self._settings, self._data, self._cache, self._util, self._log)
        self._export = RootBuilderExport(self._organiser, self._settings, self._util, self._log)
        self._legacy = RootBuilderLegacy(self._organiser, self._settings, self._util, self._log)
        super().__init__()

    def build(self):
        """Runs a full build using the current settings."""
        # Generate new build data for what we're about to do.
        hasExistingBuild = self._data.dataFileExists()
        self._log.info("Generating root mod build data.")
        newBuildData = self._data.generateBuildData()

        # Generate a full or partial set of file hashes.
        self._log.info("Updating cache.")
        fullCache = self._cache.updateCache()
        self._cache.saveCacheFile(fullCache)

        # Generate a full or partial backup.
        if self._settings.backup():
            self._log.info("Checking for updates to backup files.")
            self._backup.updateBackup()
        else:
            # Calculate any possible overwrites for if we need to update our backup or cache.
            gamePath = Path(self._strings.gamePath)
            possibleOverwrites = []
            for fileKey in newBuildData[self._data._copyKey]:
                relativePath = newBuildData[self._data._copyKey][fileKey][self._data._relativeKey]
                destPath = gamePath / relativePath
                possibleOverwrites.append(str(destPath))
            for fileKey in newBuildData[self._data._linkKey]:
                relativePath = newBuildData[self._data._linkKey][fileKey][self._data._relativeKey]
                destPath = gamePath / relativePath
                possibleOverwrites.append(str(destPath))
            self._log.info("Backup disabled, only storing potential overwrites.")
            self._backup.createPartialBackup(possibleOverwrites)

        # Deploy any files that can go via copy or links.
        self._log.info("Deploying files for Copy mode.")
        self._builder.deployCopy(newBuildData[self._data._copyKey])
        self._log.info("Deploying files for Link mode.")
        self._builder.deployLinks(newBuildData[self._data._linkKey])

        # Update any existing build data or save the new one.
        if hasExistingBuild:
            self._log.info("Previous build data exists, updating.")
            oldBuildData = self._data.loadDataFile()
            newBuildData = self._data.mergeBuildData(oldBuildData, newBuildData)

        self._log.info("Saving build data.")
        self._data.saveDataFile(newBuildData)
        self._log.info("Build complete!")


    def sync(self):
        """Runs a sync between the game and Mod Organizer."""
        hasExistingBuild = self._data.dataFileExists()
        if hasExistingBuild:
            self._log.info("Build exists, updating mod files.")
            newData = self._builder.syncFiles()
            if not self._isClear:
                self._data.saveDataFile(newData)
            self._log.info("Sync complete!")
            
    _isClear = False
    def clear(self):
        """Runs a sync and then clears up the game folder."""
        hasExistingBuild = self._data.dataFileExists()
        if hasExistingBuild:
            # Update the files in Mod Organizer if needed.
            self._isClear = True
            self.sync()
            self._isClear = False

            # Delete any deployed files or links
            self._log.info("Clearing deployed files and links.")
            self._builder.clearFiles()

            # Restore any vanilla files from backup.
            self._log.info("Restoring files from backup.")
            self._backup.restoreBackup()

            # Cleanup any build data if it's not wanted.
            self._log.info("Cleaning up remaining files.")
            self._data.deleteDataFile()
            if not self._settings.cache():
                self._cache.deleteCacheFile()
            if not self._settings.backup():
                self._backup.deleteBackup()
            
            self._log.info("Clear complete!")

    def mappings(self):
        """Retrieves mappings for usvfs if applicable."""
        hasExistingBuild = self._data.dataFileExists()
        mappings = []
        if hasExistingBuild:
            self._log.info("Build exists, generating usvfs mappings.")
            gamePath = Path(self._strings.gamePath)
            buildData = self._data.loadDataFile()
            usvfsFiles = buildData[self._data._usvfsKey]
            for file in usvfsFiles:
                fileData = usvfsFiles[file]
                mapping = mobase.Mapping()
                mapping.source = fileData[self._data._sourceKey]
                mapping.destination = str(gamePath / fileData[self._data._relativeKey])
                mapping.isDirectory = False
                mapping.createTarget = False
                mappings.append(mapping)
            #overwrite = mobase.Mapping()
            #overwrite.source = self._strings.rbOverwritePath
            #overwrite.destination = self._strings.gamePath
            #overwrite.createTarget = True
            #overwrite.isDirectory = True
            #mappings.append(overwrite)
        self._log.info("Usvfs mappings generated!")
        return mappings
