import mobase, json, urllib.request
from ..shared.shared_utilities import SharedUtilities
from .modules.pluginfinder_paths import PluginFinderPaths
from .modules.pluginfinder_files import PluginFinderFiles

class PluginFinder():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.files = PluginFinderFiles(self.organiser)
        self.paths = PluginFinderPaths(self.organiser)
        self.utilities = SharedUtilities()
        super().__init__()

    def initialDeploy():
        jsonPath = str(Path(__file__).parent / "pluginfinder_directory.json")
        if Path(jsonPath).exists():
            self.utilities.moveTo(jsonPath, self.paths.directoryJsonPath())
        try:
            with urllib.request.urlopen(self.paths.githubDirectoryUrl) as url:
                data = json.loads(url.read().decode())
                json.dump(data, self.paths.directoryJsonPath())

