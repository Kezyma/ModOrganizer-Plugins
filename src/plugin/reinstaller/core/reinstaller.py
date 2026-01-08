import mobase, subprocess, os
from pathlib import Path
from ....common.common_log import CommonLog
from ....common.common_utilities import *
from .reinstaller_settings import ReinstallerSettings
from ..modules.reinstaller_strings import ReinstallerStrings
from ..modules.reinstaller_paths import ReinstallerPaths

class Reinstaller:
    """Core Reinstaller class that handles all plugin functionality."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = ReinstallerSettings(self._organiser)
        self._strings = ReinstallerStrings("Reinstaller", self._organiser)
        self._log = CommonLog("Reinstaller", self._settings)
        self._paths = ReinstallerPaths("Reinstaller", self._organiser, self._settings, self._strings)

    def create(self, name, file):
        backupFolderPath = Path(self._strings.pluginDataPath) / name
        destFilePath = backupFolderPath / file
        sourcePath = Path(self._strings.moDownloadsPath) / file
        copyFile(sourcePath, destFilePath)
        
        metaSourcePath = Path(Path(self._strings.moDownloadsPath) / (str(file) + ".meta"))
        if metaSourcePath.exists():
            metaDestPath = backupFolderPath / (str(file) + ".meta")
            copyFile(metaSourcePath, metaDestPath)
        return name
        
    def install(self, name, file):
        modPath = Path(self._strings.pluginDataPath) / name / file
        self._organiser.installMod(modPath, str(name))
        return name

    def delete(self, name, file):
        modPath = Path(self._strings.pluginDataPath) / name / file
        deleteFile(modPath)
        metaPath = Path(Path(self._strings.pluginDataPath) / name / (file + ".meta"))
        if metaPath.exists():
            deleteFile(metaPath)
        
        fileOptions = self._paths.getInstallerFileOptions(name)
        if (len(fileOptions) == 0):
            folderPath = Path(self._strings.pluginDataPath) / name
            deleteFolder(folderPath)
        return name
