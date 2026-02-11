import mobase
import os
from pathlib import Path
from typing import List
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from .openmwplayer_strings import OpenMWPlayerStrings
from ....common.common_log import CommonLog


class OpenMWPlayerMappings:
    """Handles USVFS mapping generation for OpenMW Player."""

    def __init__(self, organiser: mobase.IOrganizer, settings: OpenMWPlayerSettings,
                 strings: OpenMWPlayerStrings, log: CommonLog):
        self._organiser = organiser
        self._settings = settings
        self._strings = strings
        self._log = log

    def getMappings(self) -> List[mobase.Mapping]:
        """Generate all USVFS mappings. Returns empty list in legacy mode."""
        if self._settings.legacymode():
            return []

        mappings = []
        mappings.extend(self._getConfigMappings())
        mappings.extend(self._getSaveMappings())
        mappings.extend(self._getOpenMWFolderMappings())

        self._log.debug(f"Generated {len(mappings)} USVFS mappings")
        return mappings

    def _getConfigMappings(self) -> List[mobase.Mapping]:
        """Generate mappings for openmw.cfg, settings.cfg, and launcher.cfg."""
        mappings = []
        externalCfgFolder = Path(self._strings.openmwCfgPath()).parent

        # Map openmw.cfg
        customCfgPath = self._strings.customOpenmwCfgPath()
        if Path(customCfgPath).exists():
            mapping = mobase.Mapping()
            mapping.source = customCfgPath
            mapping.destination = str(externalCfgFolder / "openmw.cfg")
            mapping.isDirectory = False
            mapping.createTarget = False
            mappings.append(mapping)
            self._log.debug(f"Config mapping: {customCfgPath} -> {mapping.destination}")

        # Map settings.cfg
        customSettingsPath = self._strings.customSettingsCfgPath()
        if Path(customSettingsPath).exists():
            mapping = mobase.Mapping()
            mapping.source = customSettingsPath
            mapping.destination = str(externalCfgFolder / "settings.cfg")
            mapping.isDirectory = False
            mapping.createTarget = False
            mappings.append(mapping)
            self._log.debug(f"Settings mapping: {customSettingsPath} -> {mapping.destination}")

        # Map launcher.cfg
        customLauncherPath = self._strings.customLauncherCfgPath()
        if Path(customLauncherPath).exists():
            mapping = mobase.Mapping()
            mapping.source = customLauncherPath
            mapping.destination = str(externalCfgFolder / "launcher.cfg")
            mapping.isDirectory = False
            mapping.createTarget = False
            mappings.append(mapping)
            self._log.debug(f"Launcher mapping: {customLauncherPath} -> {mapping.destination}")

        return mappings

    def _getSaveMappings(self) -> List[mobase.Mapping]:
        """Generate mappings for saves/screenshots folders if profile saves enabled."""
        mappings = []
        profile = self._organiser.profile()

        if not profile.localSavesEnabled():
            return mappings

        localSavesPath = Path(self._strings.localSavesPath())
        externalCfgFolder = Path(self._strings.openmwCfgPath()).parent

        # Ensure local saves path exists
        if not localSavesPath.exists():
            os.makedirs(localSavesPath, exist_ok=True)

        # Map saves folder (create source if needed for writes to work)
        savesSource = localSavesPath / "saves"
        if not savesSource.exists():
            os.makedirs(savesSource, exist_ok=True)

        mapping = mobase.Mapping()
        mapping.source = str(savesSource)
        mapping.destination = str(externalCfgFolder / "saves")
        mapping.isDirectory = True
        mapping.createTarget = True
        mappings.append(mapping)
        self._log.debug(f"Saves mapping: {savesSource} -> {mapping.destination}")

        # Map screenshots folder if it exists (don't create if not present)
        screenshotsSource = localSavesPath / "screenshots"
        if screenshotsSource.exists():
            mapping = mobase.Mapping()
            mapping.source = str(screenshotsSource)
            mapping.destination = str(externalCfgFolder / "screenshots")
            mapping.isDirectory = True
            mapping.createTarget = True
            mappings.append(mapping)
            self._log.debug(f"Screenshots mapping: {screenshotsSource} -> {mapping.destination}")

        return mappings

    def _getOpenMWFolderMappings(self) -> List[mobase.Mapping]:
        """Generate mappings for OpenMW folders in mods to OpenMW installation."""
        mappings = []
        openmwExePath = self._settings.openmwexepath()

        if not openmwExePath or not Path(openmwExePath).exists():
            return mappings

        openmwInstallFolder = Path(openmwExePath).parent
        self._log.debug(f"OpenMW install folder: {openmwInstallFolder}")

        # Collect all files to map (with priority - later sources win)
        fileMap = {}  # relativePath -> sourcePath

        # Process in priority order: game data (lowest), then mods by priority, then overwrite (highest)
        searchPaths = []

        # 1. Game data folder (lowest priority)
        searchPaths.append(self._strings.gameDataPath)

        # 2. Enabled mods in priority order
        modList = self._organiser.modList().allModsByProfilePriority(self._organiser.profile())
        for mod in modList:
            modState = self._organiser.modList().state(mod)
            if modState & mobase.ModState.ACTIVE:
                modPath = Path(self._strings.moModsPath) / mod
                searchPaths.append(str(modPath))

        # 3. Overwrite folder (highest priority)
        searchPaths.append(self._strings.moOverwritePath)

        # Scan each path for OpenMW folder
        for searchPath in searchPaths:
            # Check for both "OpenMW" and "openmw" (case-insensitive on Windows, but be explicit)
            for folderName in ["OpenMW", "openmw"]:
                openmwFolder = Path(searchPath) / folderName
                if openmwFolder.exists() and openmwFolder.is_dir():
                    self._log.debug(f"Found OpenMW folder: {openmwFolder}")
                    self._collectFolderFiles(openmwFolder, openmwInstallFolder, fileMap)
                    break  # Only process one case variant per search path

        # Convert fileMap to mappings
        for relativePath, sourcePath in fileMap.items():
            mapping = mobase.Mapping()
            mapping.source = sourcePath
            mapping.destination = str(openmwInstallFolder / relativePath)
            mapping.isDirectory = False
            mapping.createTarget = False
            mappings.append(mapping)

        self._log.debug(f"Generated {len(mappings)} OpenMW folder mappings")
        return mappings

    def _collectFolderFiles(self, sourceFolder: Path, destFolder: Path, fileMap: dict):
        """Recursively collect files from source folder, updating fileMap with priority."""
        for item in sourceFolder.rglob("*"):
            if item.is_file():
                relativePath = item.relative_to(sourceFolder)
                # Later sources overwrite earlier ones (priority handling)
                # Use lowercase key for case-insensitive deduplication
                fileMap[str(relativePath).lower()] = str(item)
