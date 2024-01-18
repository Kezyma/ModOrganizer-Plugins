from pathlib import Path
from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
from .rootbuilder_backup import RootBuilderBackup
from ...shared.shared_utilities import SharedUtilities
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
import mobase, os, json

class RootBuilderCopy():
    """ Root Builder copy module. Used to copy files to and from mod folders. """

    def __init__(self, organiser=mobase.IOrganizer, settings=RootBuilderSettings,paths=RootBuilderPaths,files=RootBuilderFiles,backup=RootBuilderBackup):
        self.organiser = organiser
        self.settings = settings
        self.paths = paths
        self.files = files
        self.backup = backup
        self.utilities = SharedUtilities()
        super().__init__()

    def logMessage(self, message):
        if self.settings.debug():
            self.utilities.debugMsg("[RootBuilder]" + message)

    def build(self):
        """ Copies root mod files to the game folder """
        # Check for existing data and load it.
        fileData = self.getModData()
        # Get list of current mod files.
        modFiles = self.files.getRootModFiles()
        # Iterate over current mod files and update our data.
        for file in modFiles:
            relativePath = self.paths.rootRelativePath(file)
            modFileData = {
                    "Path" : str(file),
                    "Hash" : str(self.utilities.hashFile(file))
                }
            # If this is already in our data, compare them, update if newer.
            if str(relativePath) in fileData:
                if fileData[str(relativePath)]["Hash"] != modFileData["Hash"]:
                    fileData[str(relativePath)] = modFileData
            # If the file is not in the existing data, add it.
            else:
                fileData.update({str(relativePath):modFileData})
        # Copy all mod files into the game folder
        for relativePath in fileData.keys():
            sourcePath = Path(fileData[relativePath]["Path"])
            destPath = self.paths.gamePath() / relativePath
            if sourcePath.exists():
                if not destPath.parent.exists():
                    os.makedirs(destPath.parent)
                #qInfo(u"Copying from " + str(sourcePath))
                try:
                    self.utilities.copyTo(sourcePath, destPath)
                except:
                    qInfo("Could not copy a file during build.")
        # Save data
        self.saveModData(fileData)
        return
    
    def sync(self):
        """ Copies changed mod files back to their original mod folders. """
        # Only run if there's already data.
        self.logMessage("[Copy] Synchronising files with Mod Organizer.")
        if self.hasModData():
            # Get existing data
            self.logMessage("[Copy] Mod data exists, continuing sync.")
            modData = self.getModData()
            backupData = self.backup.getFileData()
            gameFiles = self.files.getGameFileList()
            for file in gameFiles:
                self.logMessage("[Copy] Checking file: " + str(file))
                relativePath = self.paths.gameRelativePath(file)
                if str(relativePath) in modData:
                    self.logMessage("[Copy] Mod file detected: " + str(relativePath))
                    fileHash = str(self.utilities.hashFile(file))
                    if fileHash != modData[str(relativePath)]["Hash"]:
                        self.logMessage("[Copy] Mod file changed: " + str(relativePath))
                        destPath = Path(modData[str(relativePath)]["Path"])
                        if not destPath.parent.exists():
                            os.makedirs(destPath.parent)
                        try:
                            self.utilities.copyTo(file, destPath)
                            modData[str(relativePath)]["Hash"] = fileHash
                            self.logMessage("[Copy] Mod file syncronised: " + str(relativePath))
                        except:
                            self.logMessage("[Copy] Could not syncronise: " + str(relativePath))
                elif str(file) in backupData:
                    self.logMessage("[Copy] Game file detected: " + str(file))
                    fileHash = str(self.utilities.hashFile(file))
                    if fileHash != backupData[str(file)]:
                        self.logMessage("[Copy] Game file changed: " + str(relativePath))
                        overwritePath = self.paths.rootOverwritePath() / relativePath
                        if not overwritePath.parent.exists():
                            os.makedirs(overwritePath.parent)
                        try:
                            self.utilities.copyTo(file, overwritePath)
                            modData[str(relativePath)] = { "Path" : str(overwritePath), "Hash" : fileHash }
                            self.logMessage("[Copy] Game file syncronised: " + str(relativePath))
                        except:
                            self.logMessage("[Copy] Could not syncronise: " + str(relativePath))
                else:
                    self.logMessage("[Copy] New file detected: " + str(relativePath))
                    overwritePath = self.paths.rootOverwritePath() / relativePath
                    if not overwritePath.parent.exists():
                        os.makedirs(overwritePath.parent)
                    try:
                        self.utilities.copyTo(file, overwritePath)
                        modData.update({str(relativePath): {"Path": str(overwritePath), "Hash": self.utilities.hashFile(file)}})
                        self.logMessage("[Copy] New file syncronised: " + str(relativePath))
                    except:
                        self.logMessage("[Copy] Could not syncronise: " + str(relativePath))
            self.logMessage("[Copy] Updating mod data.")
            self.saveModData(modData)
            self.logMessage("[Copy] Mod data updated.")
        return

    def clear(self):
        """ Cleans up the game folder of any copied mod files, updating the originals where they have changed. """
        # Only run if there's already data.
        if self.hasModData():
            # Run a sync to update any existing mod files before deleting the game folder versions.
            self.sync()
            # Get existing data
            fileData = self.getModData()
            for relativePath in fileData.keys():
                gamePath = self.paths.gamePath() / relativePath
                # If the file exists in the game, delete it.
                if gamePath.exists():
                    #qInfo(u"Clearing file " + str(gamePath))
                    try:
                        self.utilities.deletePath(gamePath)
                    except:
                        qInfo("Could not clear a file.")
            # Clear the existing mod data
            self.clearModData()
        return

    def hasModData(self):
        """ Checks if mod file data exists. """
        return self.paths.rootModDataFilePath().exists()

    def getModData(self):
        """ Gets a dictionary of existing mod files with their hashes. """
        fileData = {}
        # If we have already run a build, just load the data from that.
        if (self.paths.rootModDataFilePath().exists()):
            try:
                fileData = json.load(open(self.paths.rootModDataFilePath(),"r", encoding="utf-8"))
            except:
                qInfo("Could not load build info.")

        return fileData

    def saveModData(self, fileData=dict):
        """ Saves current mod data. """
        if self.paths.rootModDataFilePath().exists():
            self.paths.rootModDataFilePath().touch()
        try:
            with open(self.paths.rootModDataFilePath(), "w", encoding="utf-8") as rcJson:
                json.dump(fileData, rcJson)
        except:
            qInfo("Could not save build info.")

    def clearModData(self):
        """ Removes any existing mod data. """
        if self.paths.rootModDataFilePath().exists():
            try:
                self.utilities.deletePath(self.paths.rootModDataFilePath())
            except:
                qInfo("Could not delete build info.")


    