from pathlib import Path
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
from ...shared.shared_utilities import SharedUtilities
import mobase, os, json
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class RootBuilderLinker():
    """ Root Builder link module. Used to create links for specific file types. """

    def __init__(self, organiser=mobase.IOrganizer, paths=RootBuilderPaths, files=RootBuilderFiles):
        self.organiser = organiser
        self.paths = paths
        self.files = files
        self.utilities = SharedUtilities()
        super().__init__()

    def build(self):
        """ Generates links for all linkable mod files and saves records of each of them """
        # Get all linkable mod files.
        linkFileData = self.files.getLinkableModFiles()
        for file in linkFileData:
            relativePath = self.paths.rootRelativePath(file)
            gamePath = self.paths.gamePath() / relativePath
            # If the linkable file is already in the game folder, rename it.
            if gamePath.exists():
                qInfo("Renaming for link " + str(gamePath))
                self.utilities.moveTo(gamePath, Path(str(gamePath) + ".rbackup"))
            # Create the dirs if they don't exist.
            if not gamePath.parent.exists():
                os.makedirs(gamePath.parent)
            # Try and create a link. This will fail if a link is already there.
            qInfo("Creating link for " + str(gamePath))
            Path(file).link_to(gamePath)
        # Save our link data.
        if not self.paths.rootLinkDataFilePath().exists():
            self.paths.rootLinkDataFilePath().touch()
        with open(self.paths.rootLinkDataFilePath(), "w") as jsonFile:
            json.dump(linkFileData, jsonFile)

    def clear(self):
        """ Clears any created links from mod files """
        # Check if we have any link data and load it if we do.
        if self.paths.rootLinkDataFilePath().exists():
            linkFileData = json.load(open(self.paths.rootLinkDataFilePath()))
            # Loop through our link data and unlink individual files.
            for file in linkFileData:
                relativePath = self.paths.rootRelativePath(file)
                gamePath = self.paths.gamePath() / relativePath
                if gamePath.exists():
                    qInfo("Removing link for " + str(gamePath))
                    gamePath.unlink(True)
                if Path(str(gamePath) + ".rbackup").exists():
                    qInfo("Renaming from link " + str(gamePath))
                    self.utilities.moveTo(Path(str(gamePath) + ".rbackup"), gamePath)
            # Remove our link data file.
            self.utilities.deletePath(self.paths.rootLinkDataFilePath())
