import mobase, os
from pathlib import Path
from os import listdir
from .reinstaller_paths import ReinstallerPaths
from .reinstaller_settings import ReinstallerSettings
from ...shared.shared_files import SharedFiles

class ReinstallerFiles(SharedFiles):
    """ Reinstaller file module. Used to get collections of files from different game paths. """

    def __init__(self, organiser=mobase.IOrganizer, paths=ReinstallerPaths):
        self.paths = paths
        super().__init__("Reinstaller", organiser)

    def getDownloadFileOptions(self):
        downloadFiles = self.getFolderFileList(self.paths.downloadsPath())
        modFiles = []
        for file in downloadFiles:
            if not str(file).endswith('.meta') and not str(file).endswith('.unfinished'):
                modFiles.append(str(os.path.basename(file)))
        return modFiles

    def getInstallerOptions(self):
        installers = self.getSubFolderList(self.paths.pluginDataPath())
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))
        return names

    def getInstallerFileOptions(self, name):
        installerOpts = self.getFolderFileList(self.paths.pluginDataPath() / name)
        files = []
        for file in installerOpts:
            if not str(file).endswith('.meta'):
                files.append(str(file))
        return files
