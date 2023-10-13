from pathlib import Path
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
from .rootbuilder_settings import RootBuilderSettings
from ...shared.shared_utilities import SharedUtilities
import mobase, os, json
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class RootBuilderLinker():
    """ Root Builder link module. Used to create links for specific file types. """

    def __init__(self, organiser=mobase.IOrganizer, paths=RootBuilderPaths, files=RootBuilderFiles, settings=RootBuilderSettings):
        self.organiser = organiser
        self.paths = paths
        self.files = files
        self.settings = settings
        self.utilities = SharedUtilities()
        super().__init__()

    def build(self):
        """ Generates links for all linkable mod files and saves records of each of them """
        # Get all linkable mod files.
        linkFileData = []
        if self.settings.linkonlymode():
            linkFileData = self.files.getRootModFiles()
        else:
            linkFileData = self.files.getLinkableModFiles()
        linkOutputData = []
        for file in linkFileData:
            relativePath = self.paths.rootRelativePath(file)
            gamePath = self.paths.gamePath() / relativePath
            file_path = Path(file)
            # If the linkable file is already in the game folder, rename it.
            create_link = True
            if gamePath.exists():
                if gamePath.samefile(file_path):
                    create_link = False
                else:
                    #qInfo("Renaming for link " + str(gamePath))
                    self.utilities.moveTo(gamePath, Path(str(gamePath) + ".rbackup"))
            if create_link:
                # Create the dirs if they don't exist.
                if not gamePath.parent.exists():
                    os.makedirs(gamePath.parent)
                # Try and create a link. This will fail if a link is already there.
                #qInfo("Creating link for " + str(gamePath))
                file_path.link_to(gamePath)
            mapping = {
                "Source": str(file),
                "Destination": str(gamePath)
            }
            linkOutputData.append(mapping)
        # Save our link data.
        if not self.paths.rootLinkDataFilePath().exists():
            self.paths.rootLinkDataFilePath().touch()
        with open(self.paths.rootLinkDataFilePath(), "w", encoding="utf-8") as jsonFile:
            json.dump(linkOutputData, jsonFile)

    def clear(self):
        """ Clears any created links from mod files """
        # Check if we have any link data and load it if we do.
        if self.paths.rootLinkDataFilePath().exists():
            linkFileData = json.load(open(self.paths.rootLinkDataFilePath(),"r", encoding="utf-8"))
            # Loop through our link data and unlink individual files.
            for file in linkFileData:
                destPath = Path(file["Destination"])
                srcPath = Path(file["Source"])
                if destPath.exists():
                    if os.stat(destPath).st_nlink <= 1:
                        self.utilities.moveTo(destPath, srcPath)
                    else:
                        #qInfo("Removing link for " + str(gamePath))
                        destPath.unlink(True)
                if Path(str(destPath) + ".rbackup").exists():
                    #qInfo("Renaming from link " + str(gamePath))
                    self.utilities.moveTo(Path(str(destPath) + ".rbackup"), destPath)
            # Remove our link data file.
            self.utilities.deletePath(self.paths.rootLinkDataFilePath())
