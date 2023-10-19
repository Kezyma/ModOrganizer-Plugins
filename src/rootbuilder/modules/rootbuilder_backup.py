from shutil import copy2
from pathlib import Path
from ...shared.shared_utilities import SharedUtilities
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
import mobase, os, hashlib, json, shutil, stat
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class RootBuilderBackup():
    """ Root Builder backup module. Used to back up and restore vanilla game installations. """

    def __init__(self, organiser=mobase.IOrganizer, settings=RootBuilderSettings, paths=RootBuilderPaths, files=RootBuilderFiles):
        self.organiser = organiser
        self.settings = settings
        self.paths = paths
        self.files = files
        self.utilities = SharedUtilities()
        super().__init__()

    def logMessage(self, message):
        if self.settings.debug():
            self.utilities.debugMsg("[RootBuilder]" + message)

    def backup(self):
        """ Backs up base game files, or conflicts if backup is disabled. """
        # Get hashes for our current vanilla game install
        fileData = self.getFileData()
        # Identify the files we're going to back up
        backupFiles = self.getBackupList(fileData)
        # Back up our files
        self.backupFileList(backupFiles)
        # Save the current data
        self.saveFileData(fileData)

    def restore(self):
        """ Restores the game to the most vanilla state possible, copying changes to overwrite. """
        # Check if it's possible to restore.
        self.logMessage("[Backup] Checking for backup files to restore.")
        if self.canRestore():
            self.logMessage("[Backup] Backup data exists, attempting restore.")
            if not self.paths.rootOverwritePath().exists():
                os.makedirs(self.paths.rootOverwritePath())
            # Get hashes for our current vanilla game install.
            fileData = self.getFileData()
            # Iterate through everything in the current game folder and look for changes.
            gameFiles = self.files.getGameFileList()
            self.logMessage("[Backup] Checking for new or modified game files.")
            for file in gameFiles:
                if (Path(file).exists()):
                    # If we have a record of this file, check for changes.
                    if str(file) in fileData:
                        # If file has changed, check if we have a backup.
                        if fileData[str(file)] != str(self.utilities.hashFile(file)):
                            self.logMessage("[Backup] Game file has changed: " + str(file))
                            backupPath = self.paths.rootBackupPath() / self.paths.gameRelativePath(file)
                            # If we have a backup, move the file to overwrite and restore.
                            if backupPath.exists():
                                self.logMessage("[Backup] Backup exists: " + str(backupPath))
                                overwritePath = self.paths.rootOverwritePath() / self.paths.gameRelativePath(file)
                                try:
                                    self.utilities.moveTo(str(file), str(overwritePath))
                                    self.utilities.copyTo(str(backupPath), str(file))#
                                    self.logMessage("[Backup] File restored: " + str(file))
                                except:
                                    self.logMessage("[Backup] Could not restore: " + str(file))
                            else:
                                self.logMessage("[Backup] Backup does not exist: " + str(backupPath))
                    # If this is a new file, move it to overwrite.
                    else:
                        self.logMessage("[Backup] New file found: " + str(file))
                        overwritePath = self.paths.rootOverwritePath() / self.paths.gameRelativePath(file)
                        try:
                            self.utilities.moveTo(str(file), str(overwritePath))
                            self.logMessage("[Backup] Moved to overwrite: " + str(file))
                        except:
                            self.logMessage("[Backup] Could not move to overwrite: " + str(file))
            # Iterate through the files we've got data for.
            self.logMessage("[Backup] Checking for deleted game files.")
            for file in fileData.keys():
                # Check to see if the file has been deleted.
                if not Path(file).exists():
                    self.logMessage("[Backup] File missing: " + str(file))
                    backupPath = self.paths.rootBackupPath() / self.paths.gameRelativePath(file)
                    # If the file has been deleted and has a backup, restore it.
                    if backupPath.exists():
                        #qInfo(u"Backup exists, restoring " + str(file))
                        try:
                            self.utilities.copyTo(str(backupPath), str(file))
                            self.logMessage("[Backup] File restored: " + str(file))
                        except:
                            self.logMessage("[Backup] File could not be restored: " + str(file))
                    else:
                        self.logMessage("[Backup] Backup does not exist: " + str(backupPath))
        else:
            self.logMessage("[Backup] No backup data exists.")

        # Clean up any empty game folders.
        self.logMessage("[Backup] Cleaning up empty folders.")
        gameFolders = self.files.getGameFolderList()
        for folder in gameFolders:
            if folder.exists():
                if len(self.files.getFolderFileList(folder)) == 0:
                    try:
                        shutil.rmtree(folder)
                        self.logMessage("[Backup] Cleaned up folder: " + str(folder))
                    except:
                        self.logMessage("[Backup] Could not clean up folder: " + str(folder))
        # If backup is disabled, we can clear any backed up files now that the restore is complete.

        if self.settings.backup() is False:
            self.logMessage("[Backup] Backup disabled, removing any existing backup files.")
            self.clearBackupFiles()

        # Delete current backup data.
        self.logMessage("[Backup] Deleting exising backup file data.")
        self.clearFileData()
        
    def backupFileList(self, backupFiles=list):
        """ Backs up a list of game files if not already backed up. """
        # Loop through our list of files.
        self.logMessage("[Backup] Backing up files.")
        for file in backupFiles:
            relativePath = self.paths.gameRelativePath(file)
            backupPath = self.paths.rootBackupPath() / relativePath
            # Back them up if they don't already exist.
            if not backupPath.exists() and Path(file).exists():
                #qInfo(u"Backing up " + str(file))
                try:
                    self.logMessage("[Backup] Backing up file: " + str(file))
                    self.utilities.copyTo(str(file), str(backupPath))
                except:
                    self.logMessage("[Backup] Could not create backup: " + str(file))
        self.logMessage("[Backup] File backup complete.")

    def getBackupList(self, fileData=dict):
        """ Gets a list of files that should be backed up. """
        backupFiles = []
        self.logMessage("[Backup] Compiling list of files to backup.")
        # If backup is enabled, we want to back up all the vanilla files.
        if self.settings.backup():
            self.logMessage("[Backup] Backup enabled, backing up all game files.")
            backupFiles = fileData.keys()
        # Otherwise, we need to identify which files are going to conflict.
        else:
            self.logMessage("[Backup] Backup disabled, only backing up conflict files.")
            conflictFiles = []
            # If we're in linkmode, only linked files could cause conflicts.
            if self.settings.linkmode() or self.settings.linkonlymode():
                self.logMessage("[Backup] Link mode enabled, only checking for link conflicts.")
                conflictFiles = self.files.getLinkableModFiles()
            # Otherwise, every root mod file could be a conflict.
            else:
                self.logMessage("[Backup] Link mode disabled, checking for all conflicts.")
                conflictFiles = self.files.getRootModFiles()
            # Loop through the mod files and see if we have data for them.
            for file in conflictFiles:
                self.logMessage("[Backup] Checking for file conflict: " + str(file))
                relativePath = self.paths.rootRelativePath(file)
                gamePath = self.paths.gamePath() / relativePath
                # If we have data, we need to back this file up.
                if str(gamePath) in fileData:
                    self.logMessage("[Backup] File conflict found: " + str(file))
                    backupFiles.append(gamePath)

        self.logMessage("[Backup] Backup file list compiled.")
        return backupFiles

    def getFileData(self):
        """ Gets a dictionary of vanilla game files with their hashes. """
        fileData = {}
        success = False
        self.logMessage("[Backup] Loading file data.")
        # If we have a cache file for this game already load that.
        if (self.settings.cache() and self.paths.rootCacheFilePath().exists()):
            try:
                self.logMessage("[Backup] Cache file found, attempting to load.")
                fileData = json.load(open(self.paths.rootCacheFilePath(),"r", encoding="utf-8"))
                self.logMessage("[Backup] Cache file loaded successfully.")
                success = True
            except:
                self.logMessage("[Backup] Cache file could not be loaded, deleting cache.")
                self.utilities.deletePath(self.paths.rootCacheFilePath())
        # If we have already run a build, just load the data from that.
        if (self.paths.rootBackupDataFilePath().exists() and success == False):
            try:
                self.logMessage("[Backup] Existing backup hash file found, attempting to load.")
                fileData = json.load(open(self.paths.rootBackupDataFilePath(),"r", encoding="utf-8"))
                self.logMessage("[Backup] Existing backup hash file loaded successfully.")
                success = True
            except:
                self.logMessage("[Backup] Existing backup hash file could not be loaded, deleting cache.")
                self.utilities.deletePath(self.paths.rootBackupDataFilePath())
        # Hash the base game files.
        if (success == False):
            self.logMessage("[Backup] No existing hashes found, building file data.")
            fileData = self.buildCache()

        gamePath = str(self.paths.gamePath())
        for file in list(fileData.keys()):
            if not file.startswith(gamePath):
                fullPath = os.path.join(gamePath, file)
                fileData[fullPath] = fileData.pop(file)

        self.logMessage("[Backup] File data loaded.")
        return fileData

    def saveFileData(self, fileData=dict):
        """ Saves current file data to the backup data path """
        self.logMessage("[Backup] Saving backup data file.")
        if self.paths.rootBackupDataFilePath().exists():
            self.paths.rootBackupDataFilePath().touch()
        try:
            with open(self.paths.rootBackupDataFilePath(), "w", encoding="utf-8") as rcJson:
                json.dump(fileData, rcJson)
            self.logMessage("[Backup] Backup data file saved.")
        except:
            self.logMessage("[Backup] Could not save backup data file.")

    def clearFileData(self):
        """ Clears the current backup data file """
        if self.paths.rootBackupDataFilePath().exists():
            try:
                self.utilities.deletePath(self.paths.rootBackupDataFilePath())
                self.logMessage("[Backup] Backup data file deleted.")
            except:
                self.logMessage("[Backup] Could not delete backup file data.")

    def clearBackupFiles(self):
        """ Clears the current backup file folder """
        if self.paths.rootBackupPath().exists():
            try:
                shutil.rmtree(self.paths.rootBackupPath())
                self.logMessage("[Backup] Deleted backup files.")
            except:
                self.logMessage("[Backup] Could not delete backup files.")

    def clearAllBackupFiles(self):
        """ Clears backup files for all versions. """
        paths = self.paths.rootBackupPathAllVersions()
        if paths and len(paths) > 0:
            for path in paths:
                try:
                    shutil.rmtree(str(path))
                    self.logMessage("[Backup] Deleted backup files: " + str(path))
                except:
                    self.logMessage("[Backup] Could not delete backup files: " + str(path))

    def buildCache(self):
        """ Triggers a cache build if none exists """
        fileData = {}
        gamePath = self.paths.gamePath()
        self.logMessage("[Backup] Building file hash collection.")
        for file in self.files.getGameFileList():
            self.logMessage("[Backup] Hashing file: " + str(file))
            relPath = os.path.relpath(str(file),str(gamePath))
            fileData.update({str(relPath):str(self.utilities.hashFile(file))})

        # If cache is enabled, save the data to cache.
        if self.settings.cache():
            self.logMessage("[Backup] Cache enabled, saving cache file.")
            if not self.paths.rootCacheFilePath().exists():
                self.paths.rootCacheFilePath().touch()
            try:
                with open(self.paths.rootCacheFilePath(), "w", encoding="utf-8") as rcJson:
                    json.dump(fileData, rcJson)
                self.logMessage("[Backup] Cache file saved successfully.")
            except:
                self.logMessage("[Backup] Cache file could not be saved.")
        # Otherwise, clear any cache if it exists.
        else:
            self.logMessage("[Backup] Cache disabled, deleting any existing file.")
            self.clearCache()
        
        self.logMessage("[Backup] File hash collection built.")
        return fileData

    def clearCache(self):
        """ Clears the current cache file """
        if self.paths.rootCacheFilePath().exists():    
            try:
                self.utilities.deletePath(self.paths.rootCacheFilePath())
            except:
                self.logMessage("[Backup] Could not delete cache file.")

    def clearAllCache(self):
        """ Clears cache files for all versions. """
        paths = self.paths.rootCacheFilePathAllVersions()
        if paths and len(paths) > 0:
            for path in paths:
                try:
                    self.utilities.deletePath(str(path))
                except:
                    self.logMessage("[Backup] Could not delete cache file: " + str(path))

    def canRestore(self):
        """ Checks if backup data exists and therefore whether a restore is possible """
        # We can attempt to restore as long as we have some data, either from a current run or from cache
        # We don't want to run this if we don't have data and risk generating data from a contaminated install
        #qInfo("Checking " + str(self.paths.rootBackupDataFilePath()))
        #qInfo("Checking" + str(self.paths.rootCacheFilePath()))
        backupDataExists = self.paths.rootBackupDataFilePath().exists()
        cacheDataExists = self.paths.rootCacheFilePath().exists()
        return backupDataExists or cacheDataExists


            


