import mobase, shutil
from pathlib import Path
from .modules.reinstaller_paths import ReinstallerPaths
from .modules.reinstaller_files import ReinstallerFiles
from ..shared.shared_utilities import SharedUtilities

class Reinstaller():

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.paths = ReinstallerPaths(self.organiser)
        self.files = ReinstallerFiles(self.organiser)
        self.utilities = SharedUtilities()
        super().__init__()
        
    def create(self, name, file):
        backupFolderPath = self.paths.pluginDataPath() / name
        destFilePath = backupFolderPath / file
        self.utilities.copyTo(self.paths.downloadsPath() / file, destFilePath)
        if Path(self.paths.downloadsPath() / (str(file) + ".meta")).exists():
            self.utilities.copyTo(self.paths.downloadsPath() / (str(file) + ".meta"), backupFolderPath / (str(file) + ".meta"))
        return name
        
    def install(self, name, file):
        self.organiser.installMod(str(self.paths.pluginDataPath() / name / file), str(name))
        return name

    def delete(self, name, file):
        self.utilities.deletePath(self.paths.pluginDataPath() / name / file)
        metaPath = self.paths.pluginDataPath() / name / (str(file) + ".meta")
        if (Path(metaPath).exists()):
            self.utilities.deletePath(metaPath)
        fileOptions = self.files.getInstallerFileOptions(name)
        if (len(fileOptions) == 0):
            shutil.rmtree(self.paths.pluginDataPath() / name)
        return name