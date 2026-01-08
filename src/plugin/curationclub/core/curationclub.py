"""Curation Club core class."""

import mobase
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from ....common.common_log import CommonLog
from ....common.common_utilities import loadJson, saveJson, copyFile, moveFile, deleteFile
from .curationclub_settings import CurationClubSettings
from ..modules.curationclub_strings import CurationClubStrings
from ..modules.curationclub_scanner import CurationClubScanner
from ..models.curationclub_creationdata import CreationData, CREATION_ID, CREATION_NAME, CREATION_FILES, CREATION_MANUAL
from ..models.curationclub_curationdata import (
    CurationData, CurationState, createCurationData, createCurationState,
    CURATION_SOURCE_FILES, CURATION_DEST_FILES, CURATION_MOD_NAME
)


class CurationClub:
    """Core Curation Club class that handles all plugin functionality."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = CurationClubSettings(self._organiser)
        self._log = CommonLog("CurationClub", self._settings)
        self._strings = CurationClubStrings("CurationClub", self._organiser)
        self._scanner = CurationClubScanner(self._organiser, self._strings, self._log)
        self._creationsCache = None
        self._curationState = None

    def loadCreationsDatabase(self, reload: bool = False) -> Dict[str, CreationData]:
        """
        Loads the creations database, merging cached data with manual additions.
        Manual additions are preserved when cache is updated.
        """
        if self._creationsCache is not None and not reload:
            return self._creationsCache

        # Load the default/cached database
        cachedPath = self._strings.creationsDatabasePath
        cached = loadJson(cachedPath) or {}

        # Load manual additions
        manualPath = self._strings.manualCreationsPath
        manual = loadJson(manualPath) or {}

        # Merge: manual entries override cached ones
        self._creationsCache = {}

        # Add all cached entries
        for cid, data in cached.items():
            self._creationsCache[cid] = data
            self._creationsCache[cid][CREATION_MANUAL] = False

        # Add/override with manual entries
        for cid, data in manual.items():
            self._creationsCache[cid] = data
            self._creationsCache[cid][CREATION_MANUAL] = True

        return self._creationsCache

    def saveManualCreation(self, creation: CreationData) -> bool:
        """Saves a manually added creation to the manual creations file."""
        manualPath = self._strings.manualCreationsPath
        manual = loadJson(manualPath) or {}

        creation[CREATION_MANUAL] = True
        manual[creation[CREATION_ID]] = creation

        if saveJson(manualPath, manual):
            # Reload cache
            self._creationsCache = None
            self.loadCreationsDatabase(reload=True)
            return True
        return False

    def deleteManualCreation(self, creationId: str) -> bool:
        """Removes a manually added creation."""
        manualPath = self._strings.manualCreationsPath
        manual = loadJson(manualPath) or {}

        if creationId in manual:
            del manual[creationId]
            if saveJson(manualPath, manual):
                self._creationsCache = None
                self.loadCreationsDatabase(reload=True)
                return True
        return False

    def loadCurationState(self, reload: bool = False) -> CurationState:
        """Loads the curation state tracking what has been curated."""
        if self._curationState is not None and not reload:
            return self._curationState

        statePath = self._strings.curationStatePath
        self._curationState = loadJson(statePath)

        if self._curationState is None:
            self._curationState = createCurationState()

        return self._curationState

    def saveCurationState(self) -> bool:
        """Saves the current curation state."""
        statePath = self._strings.curationStatePath
        return saveJson(statePath, self._curationState)

    def scanForCreations(self) -> Tuple[List[CreationData], List[str]]:
        """
        Scans the game Data folder for Creation Club content.
        Returns tuple of (matched_creations, unmatched_files).
        """
        database = self.loadCreationsDatabase()
        return self._scanner.scanGameFolder(database)

    def getCreationModName(self, creation: CreationData) -> str:
        """Gets the mod name for a creation based on current settings."""
        if self._settings.groupmode() == "single":
            return self._settings.combinedname()

        nameFormat = self._settings.nameformat()
        name = nameFormat.replace("{NAME}", creation[CREATION_NAME])
        name = name.replace("{ID}", creation[CREATION_ID])
        return name

    def curateCreation(self, creation: CreationData, files: List[str]) -> Optional[CurationData]:
        """
        Moves a creation's files from game Data to MO2 mod folder.
        Returns CurationData on success, None on failure.
        """
        modName = self.getCreationModName(creation)
        modsPath = Path(self._strings.moModsPath)
        modPath = modsPath / modName
        gamePath = Path(self._strings.gameDataPath)

        sourceFiles = []
        destFiles = []

        try:
            # Create mod folder if needed
            modPath.mkdir(parents=True, exist_ok=True)

            for filePath in files:
                srcPath = Path(filePath)
                if not srcPath.exists():
                    continue

                # Get relative path from game data folder
                try:
                    relativePath = srcPath.relative_to(gamePath)
                except ValueError:
                    # File not in game data folder, skip
                    continue

                destPath = modPath / relativePath
                destPath.parent.mkdir(parents=True, exist_ok=True)

                # Move the file
                if moveFile(str(srcPath), str(destPath)):
                    self._log.debug(f"Moved {srcPath} to {destPath}")
                    sourceFiles.append(str(srcPath))
                    destFiles.append(str(destPath))
                else:
                    self._log.warning(f"Failed to move {srcPath}")

            if not destFiles:
                self._log.warning(f"No files moved for {creation[CREATION_NAME]}")
                return None

            # Create curation data
            curation = createCurationData(
                id=creation[CREATION_ID],
                name=creation[CREATION_NAME],
                modName=modName,
                sourceFiles=sourceFiles,
                destFiles=destFiles,
                timestamp=datetime.now().isoformat()
            )

            # Update state
            state = self.loadCurationState()
            state["curations"][creation[CREATION_ID]] = curation
            self.saveCurationState()

            self._log.info(f"Curated {creation[CREATION_NAME]} to {modName}")
            return curation

        except Exception as e:
            self._log.warning(f"Error curating {creation[CREATION_NAME]}: {e}")
            return None

    def curateAll(self, creations: List[Tuple[CreationData, List[str]]]) -> int:
        """
        Curates all provided creations.
        Returns count of successfully curated creations.
        """
        count = 0
        for creation, files in creations:
            if self.curateCreation(creation, files):
                count += 1
        return count

    def undoCuration(self, creationId: str) -> bool:
        """
        Undoes a curation by moving files back to game Data folder.
        Returns True on success.
        """
        state = self.loadCurationState()
        if creationId not in state["curations"]:
            self._log.warning(f"No curation found for {creationId}")
            return False

        curation = state["curations"][creationId]
        sourceFiles = curation[CURATION_SOURCE_FILES]
        destFiles = curation[CURATION_DEST_FILES]

        success = True
        for srcPath, destPath in zip(sourceFiles, destFiles):
            destFilePath = Path(destPath)
            if destFilePath.exists():
                srcFilePath = Path(srcPath)
                srcFilePath.parent.mkdir(parents=True, exist_ok=True)

                if moveFile(str(destFilePath), str(srcFilePath)):
                    self._log.debug(f"Restored {destFilePath} to {srcFilePath}")
                else:
                    self._log.warning(f"Failed to restore {destFilePath}")
                    success = False

        if success:
            del state["curations"][creationId]
            self.saveCurationState()
            self._log.info(f"Undid curation for {curation[CREATION_NAME]}")

            # Clean up empty mod folder
            modPath = Path(self._strings.moModsPath) / curation[CURATION_MOD_NAME]
            self._cleanupEmptyFolder(modPath)

        return success

    def undoAll(self) -> int:
        """Undoes all curations. Returns count of successful undos."""
        state = self.loadCurationState()
        creationIds = list(state["curations"].keys())
        count = 0
        for cid in creationIds:
            if self.undoCuration(cid):
                count += 1
        return count

    def getCuratedCreations(self) -> Dict[str, CurationData]:
        """Returns dict of currently curated creations."""
        state = self.loadCurationState()
        return state["curations"]

    def isCreationCurated(self, creationId: str) -> bool:
        """Checks if a creation has been curated."""
        state = self.loadCurationState()
        return creationId in state["curations"]

    def _cleanupEmptyFolder(self, path: Path):
        """Recursively removes empty folders."""
        if not path.exists() or not path.is_dir():
            return

        # Remove empty subfolders first
        for child in path.iterdir():
            if child.is_dir():
                self._cleanupEmptyFolder(child)

        # Remove this folder if empty
        if not any(path.iterdir()):
            try:
                path.rmdir()
                self._log.debug(f"Removed empty folder {path}")
            except OSError:
                pass
