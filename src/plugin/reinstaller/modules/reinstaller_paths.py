import mobase, glob, re, os
from pathlib import Path
from .reinstaller_strings import ReinstallerStrings
from ..core.reinstaller_settings import ReinstallerSettings
from ....common.common_paths import CommonPaths
from ....common.common_log import CommonLog
from typing import List

class ReinstallerPaths(CommonPaths):
    """Reinstaller paths module, contains path related functions for Reinstaller."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:ReinstallerSettings, strings:ReinstallerStrings):
        super().__init__(plugin, organiser)
        self._strings = strings
        self._settings = settings

    def getDownloadFileOptions(self):
        downloadFiles = self.files(self._strings.moDownloadsPath)
        modFiles = []
        for file in downloadFiles:
            if not str(file).endswith('.meta') and not str(file).endswith('.unfinished'):
                modFiles.append(str(os.path.basename(file)))
        return modFiles

    metaRegex = r"^modName=(.+)$"
    def getDownloadFileName(self, downloadName=str):
        defaultName = str(downloadName).split("_")[0].split("-")[0].split(".")[0].strip()
        metaPath = str(Path(self._strings.moDownloadsPath) / (str(downloadName) + ".meta"))
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
        installers = self.subfolders(self._strings.pluginDataPath)
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))
        return names

    def getInstallerFileOptions(self, name):
        installerOpts = self.files(Path(self._strings.pluginDataPath) / name)
        files = []
        for file in installerOpts:
            if not str(file).endswith('.meta'):
                files.append(str(file))
        return files


