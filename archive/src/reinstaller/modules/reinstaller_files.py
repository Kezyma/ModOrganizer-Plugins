import mobase, os, re
from pathlib import Path
from os import listdir
from .reinstaller_paths import ReinstallerPaths
from .reinstaller_settings import ReinstallerSettings
from ...shared.shared_files import SharedFiles
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

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

    metaRegex = r"^modName=(.+)$"
    def getDownloadFileName(self, downloadName=str):
        defaultName = str(downloadName).split("_")[0].split("-")[0].split(".")[0].strip()
        metaPath = str(self.paths.downloadsPath() / (str(downloadName) + ".meta"))
        if Path(metaPath).exists():
            try:
                metaFile = open(metaPath, "r")
                metaText = metaFile.read()
                metaFile.close()
                matches = re.search(self.metaRegex, metaText, re.MULTILINE)
                if matches:
                    grp = str(matches.group(1))
                    if grp and len(grp) > 0:
                        return grp
            except:
                return defaultName
        return defaultName
    
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
