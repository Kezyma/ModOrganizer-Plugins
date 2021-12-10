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

    def initialDeploy(self):
        jsonPath = str(Path(__file__).parent / "pluginfinder_directory.json")
        if Path(jsonPath).exists():
            self.utilities.moveTo(jsonPath, self.paths.directoryJsonPath())
        #try:
        response = urllib.request.urlopen(self.paths.githubDirectoryUrl).read()
        qInfo(str(response))
        data = json.loads(response)
        json.dump(data, self.paths.directoryJsonPath())
       # except:
        #    qInfo("Could not download update.")


