from shutil import copy2
from pathlib import Path

from ...shared.shared_utilities import SharedUtilities
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
import mobase, os, hashlib, json, shutil

class RootBuilderUpdate():
    """ Root Builder update module. Used to prevent issues when games update. """

    def __init__(self, organiser=mobase.IOrganizer, paths=RootBuilderPaths,files=RootBuilderFiles):
        self.organiser = organiser
        self.paths = paths
        self.files = files
        self.utilities = SharedUtilities()
        super().__init__()

    def migrateLegacyGameData(self):
        """ Migrates pre-versioned data to the new folder. """
        # Move the backup files.
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "backup").exists():
            self.utilities.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "backup", self.paths.rootBuilderGameDataPath())

        # Move the json files.
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderCacheData.json").exists():
            self.utilities.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderCacheData.json", self.paths.rootCacheFilePath())
        
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderBackupData.json").exists():
            self.utilities.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderBackupData.json", self.paths.rootBackupDataFilePath())
        
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderModData.json").exists():
            self.utilities.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderModData.json", self.paths.rootModDataFilePath())
        
        if Path(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderLinkData.json").exists():
            self.utilities.moveTo(self.paths.rootBuilderLegacyGameDataPath() / "RootBuilderLinkData.json", self.paths.rootLinkDataFilePath())

    def hasGameUpdateBug(self):
        """ Determines if this game has the update bug. """
        legacyPath = self.paths.rootBuilderLegacyGameDataPath()
        currentPath = self.paths.rootBuilderGameDataPath() # Create it if it doesn't already exist.
        versionFolders = sorted(self.files.getSubFolderList(legacyPath, False), reverse=True)
        versionFolders.remove(currentPath)

        # If there is at least one past version of the game, it might need a fix.
        if len(versionFolders) > 0:
            hasBug = False
            # If either of the build data files are present, then we've got a bug.
            for folder in versionFolders:
                if Path(folder / "RootBuilderModData.json").exists():
                    hasBug = True
                if Path(folder / "RootBuilderLinkData.json").exists():
                    hasBug = True
                if Path(folder / "RootBuilderBackupData.json").exists():
                    hasBug = True
            return hasBug
        else:
            return False
    
    def fixGameUpdateBug(self):
        """ Moves files to try and resolve the game update bug. """
        if self.hasGameUpdateBug():
            legacyPath = self.paths.rootBuilderLegacyGameDataPath()
            currentPath = self.paths.rootBuilderGameDataPath()
            versionFolders = sorted(self.files.getSubFolderList(legacyPath, False), reverse=True)
            versionFolders.remove(currentPath)
            # If there is at least one past version of the game, it might need a fix.
            if len(versionFolders) > 0:
                # Get the current and previous version folders.
                foundBug = False
                for folder in versionFolders:
                    if not foundBug:
                        if Path(folder / "RootBuilderModData.json").exists():
                            self.utilities.moveTo(str(folder / "RootBuilderModData.json"), str(self.paths.rootModDataFilePath()))
                            foundBug = True
                        if Path(folder / "RootBuilderLinkData.json").exists():
                            self.utilities.moveTo(str(folder / "RootBuilderLinkData.json"), str(self.paths.rootLinkDataFilePath()))
                            foundBug = True
                        if Path(folder / "RootBuilderBackupData.json").exists():
                            self.utilities.moveTo(str(folder / "RootBuilderBackupData.json"), str(self.paths.rootBackupDataFilePath()))
                            foundBug = True
                        if foundBug and Path(folder / "RootBuilderCacheData.json").exists():
                            self.utilities.copyTo(str(folder / "RootBuilderCacheData.json"), str(self.paths.rootCacheFilePath()))
                        if foundBug and Path(folder / "backup").exists():
                            self.utilities.replaceDir(str(folder / "backup"), str(self.paths.rootBackupPath()))

            


