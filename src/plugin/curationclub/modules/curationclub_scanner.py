"""Curation Club scanner module for detecting Creation Club content."""

import mobase
import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Set

from ....common.common_log import CommonLog
from .curationclub_strings import CurationClubStrings
from ..models.curationclub_creationdata import CreationData, CREATION_ID, CREATION_NAME, CREATION_FILES


class CurationClubScanner:
    """Scans for Creation Club content in the game folder."""

    # Common Creation Club file patterns
    CC_PATTERNS = [
        "cc*.esl",
        "cc*.esm",
        "cc*.esp",
        "cc*.ba2",
        "cc* - *.ba2",
    ]

    # Regex to extract creation ID from filename
    CC_ID_REGEX = re.compile(r'^(cc[A-Z]{3}[A-Z0-9]{3}\d{3})', re.IGNORECASE)

    def __init__(self, organiser: mobase.IOrganizer, strings: CurationClubStrings, log: CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._log = log

    def scanGameFolder(self, database: Dict[str, CreationData]) -> Tuple[List[Tuple[CreationData, List[str]]], List[str]]:
        """
        Scans the game Data folder for Creation Club content.

        Args:
            database: Dict of known creations keyed by ID

        Returns:
            Tuple of:
            - List of (CreationData, [files]) for matched creations
            - List of unmatched CC files
        """
        dataPath = Path(self._strings.gameDataPath)
        if not dataPath.exists():
            self._log.warning(f"Game data path not found: {dataPath}")
            return [], []

        # Find all CC files
        ccFiles = self._findCCFiles(dataPath)
        self._log.debug(f"Found {len(ccFiles)} CC files in game folder")

        # Group files by creation ID
        filesByCreation = self._groupFilesByCreation(ccFiles)

        # Match to database
        matched = []
        unmatched = []

        for creationId, files in filesByCreation.items():
            if creationId in database:
                creation = database[creationId]
                matched.append((creation, files))
                self._log.debug(f"Matched creation: {creation[CREATION_NAME]} ({len(files)} files)")
            else:
                # Unknown creation - add to unmatched
                unmatched.extend(files)
                self._log.debug(f"Unknown creation ID: {creationId}")

        return matched, unmatched

    def _findCCFiles(self, dataPath: Path) -> List[str]:
        """Finds all Creation Club files in the data folder."""
        ccFiles = []

        for pattern in self.CC_PATTERNS:
            matches = glob.glob(str(dataPath / pattern), recursive=False)
            ccFiles.extend(matches)

        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for f in ccFiles:
            normalized = f.lower()
            if normalized not in seen:
                seen.add(normalized)
                unique.append(f)

        return unique

    def _groupFilesByCreation(self, files: List[str]) -> Dict[str, List[str]]:
        """Groups files by their creation ID."""
        groups = {}

        for filePath in files:
            filename = os.path.basename(filePath)
            creationId = self._extractCreationId(filename)

            if creationId:
                if creationId not in groups:
                    groups[creationId] = []
                groups[creationId].append(filePath)

        return groups

    def _extractCreationId(self, filename: str) -> str:
        """Extracts the creation ID from a filename."""
        match = self.CC_ID_REGEX.match(filename)
        if match:
            return match.group(1).lower()
        return None

    def detectCreationFromFiles(self, files: List[str]) -> Tuple[str, str]:
        """
        Attempts to detect creation info from a list of files.
        Returns (id, suggested_name) tuple.
        """
        if not files:
            return None, None

        # Get ID from first file
        filename = os.path.basename(files[0])
        creationId = self._extractCreationId(filename)

        if not creationId:
            return None, None

        # Try to extract name from ESL/ESM/ESP filename
        suggestedName = None
        for f in files:
            fname = os.path.basename(f).lower()
            if fname.endswith(('.esl', '.esm', '.esp')):
                # Format: ccXXXSSE001-Name.esl
                parts = fname.split('-', 1)
                if len(parts) > 1:
                    namePart = parts[1].rsplit('.', 1)[0]
                    suggestedName = self._formatName(namePart)
                    break

        if not suggestedName:
            suggestedName = creationId.upper()

        return creationId, suggestedName

    def _formatName(self, rawName: str) -> str:
        """Formats a raw name into a readable display name."""
        # Split on capitals and format
        # e.g., "SurvivalMode" -> "Survival Mode"
        formatted = re.sub(r'([a-z])([A-Z])', r'\1 \2', rawName)
        return formatted.title()

    def getFilesForCreation(self, creationId: str) -> List[str]:
        """Gets all files in game folder belonging to a creation."""
        dataPath = Path(self._strings.gameDataPath)
        files = []

        for pattern in self.CC_PATTERNS:
            # Modify pattern to match specific creation
            specificPattern = pattern.replace("cc*", f"{creationId}*")
            matches = glob.glob(str(dataPath / specificPattern), recursive=False)
            files.extend(matches)

        return list(set(files))
