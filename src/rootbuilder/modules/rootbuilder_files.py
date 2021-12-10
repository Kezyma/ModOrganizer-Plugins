import mobase
from pathlib import Path
from os import listdir
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_settings import RootBuilderSettings
from ...shared.shared_files import SharedFiles

class RootBuilderFiles(SharedFiles):
    """ Root Builder file module. Used to get collections of files from different game paths. """

    def __init__(self, organiser=mobase.IOrganizer, settings=RootBuilderSettings,paths=RootBuilderPaths):
        super().__init__("RootBuilder", organiser)
        self.settings = settings
        self.paths = paths

    def getGameFileList(self):
        """ Gets a list of all valid files in the current game folder. """
        # Get all the current game files.
        gameFiles = self.getFolderFileList(self.paths.gamePath())
        validFiles = []
        # Loop through files and look for invalid ones.
        for file in gameFiles:
            exclude = False
            # Check if the file is, or is in, an exclusion.
            for ex in self.settings.exclusions():
                if self.paths.sharedPath(self.paths.gamePath() / ex, file):
                    exclude = True
            # Check if the file is part of the game data.
            if self.paths.sharedPath(self.paths.gamePath() / self.paths.gameDataDir(), file):
                exclude = True
            if exclude == False:
                validFiles.append(file)
        return validFiles

    def getGameFolderList(self):
        """ Gets a list of all folders in the current game folder. """
        gameFolders = self.getSubFolderList(self.paths.gamePath())
        validFolders = []
        # Loop through folder and look for invalid ones.
        for folder in gameFolders:
            exclude = False
            # Check if the folder is, or is in, an exclusion.
            for ex in self.settings.exclusions():
                if self.paths.sharedPath(self.paths.gamePath() / ex, folder):
                    exclude = True
            # Check if the folder is part of the game data.
            if self.paths.sharedPath(self.paths.gamePath() / self.paths.gameDataDir(), folder):
                exclude = True
            if exclude == False:
                validFolders.append(folder)
        return validFolders

    def getRootMods(self):
        """ Gets a list of all active mods with valid root files. """
        # Get a list of all current mods, in order.
        modlist = self.organiser.modList().allModsByProfilePriority()
        rootmods = []
        # Loop through the list of mods.
        for mod in modlist:
            # Check that the mod is active and has a root folder.
            if self.organiser.modList().state(mod) & mobase.ModState.ACTIVE:
                if (self.paths.modsPath() / mod / "Root").exists():
                    exclude = False
                    # Check if the file is, or is in, an exclusion.
                    for ex in self.settings.exclusions():
                        if self.paths.fileExists(self.paths.modsPath() / mod / "Root" / ex):
                        #if (self.paths.modsPath() / mod / "Root" / ex).exists():
                            exclude = True
                    # Check if the file is part of the game data folder.
                    if (self.paths.modsPath() / mod / "Root" / self.paths.gameDataDir()).exists():
                        exclude = True
                    if exclude == False:
                        rootmods.append(mod)
        return rootmods

    def getRootModFiles(self):
        """ Gets a list of all root files in active mods. """
        # Get all the current mods with valid root folders.
        modlist = self.getRootMods()
        modFiles = {}
        # Loop through the modlist and get all the files from each.
        for mod in modlist:
            for file in self.getFolderFileList(self.paths.modsPath() / mod / "Root"):
                relativePath = self.paths.rootRelativePath(file)
                # If the file already exists from an earlier mod, overwrite it.
                if relativePath in modFiles:
                    modFiles[relativePath] = file
                else:
                    modFiles.update({str(relativePath):str(file)})
        # Do the same for the root overwrite folder.
        if self.paths.rootOverwritePath().exists():
            for file in self.getFolderFileList(self.paths.rootOverwritePath()):
                relativePath = self.paths.rootRelativePath(file)
                # If the file already exists from an earlier mod, overwrite it.
                if relativePath in modFiles:
                    modFiles[relativePath] = file
                else:
                    modFiles.update({str(relativePath):str(file)})
        return list(modFiles.values())

    def getLinkableModFiles(self):
        """ Gets a list of all root files in active mods that are valid for linking """
        # Get all root files in currently active mods.
        modFiles = self.getRootModFiles()
        linkableFiles = []
        # Loop through the files in each mod and look for linkable extensions.
        for file in modFiles:
            exclude = True
            # Loop through the linkable extensions and look for a match.
            for ex in self.settings.linkextensions():
                if (str(file)).endswith("." + ex):
                    exclude = False
            if exclude == False:
                linkableFiles.append(file)
        return linkableFiles

    
