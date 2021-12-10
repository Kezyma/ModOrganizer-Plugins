import mobase, json, urllib.request
from ..shared.shared_utilities import SharedUtilities
from .modules.pluginfinder_paths import PluginFinderPaths
from .modules.pluginfinder_files import PluginFinderFiles
from PyQt5.QtCore import QCoreApplication, qInfo
from pathlib import Path

class PluginFinder():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.files = PluginFinderFiles(self.organiser)
        self.paths = PluginFinderPaths(self.organiser)
        self.utilities = SharedUtilities()
        super().__init__()

    def deploy(self):
        """ Deploys the directory file to plugin data and attempts to update it. """
        # Copy the default directory over to the plugin data folder.
        jsonPath = str(Path(__file__).parent / "pluginfinder_directory.json")
        if Path(jsonPath).exists():
            self.utilities.moveTo(jsonPath, self.paths.directoryJsonPath())
        # Try and update the directory from the github repo.
        self.updateDirectory()

    def updateDirectory(self):
        """ Attempt to download a directory update from Github. """
        try:
            data = json.loads(urllib.request.urlopen(self.paths.githubDirectoryUrl).read())
            with open(self.paths.directoryJsonPath(), "w") as rcJson:
                json.dump(data, rcJson)
        except:
            qInfo("Could not download update.")
        urllib.request.urlcleanup()

    def directory(self):
        """ Get the directory as json. """
        directory = json.load(open(self.paths.directoryJsonPath()))
        return directory

    