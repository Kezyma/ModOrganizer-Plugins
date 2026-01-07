import mobase
import configparser
import os
from pathlib import Path
from typing import List, Dict, Tuple
from ..models.listexporter_modinfo import ModInfo
from .listexporter_strings import ListExporterStrings
from ....common.common_log import CommonLog
from ....common.common_utilities import loadLines


class ListExporterData:
    """Handles data collection from profiles and mods."""

    EXCLUDE_TAG = "<le_exclude>"  # Case-insensitive exclusion tag

    def __init__(self, organiser: mobase.IOrganizer, strings: ListExporterStrings, log: CommonLog):
        self._organiser = organiser
        self._strings = strings
        self._log = log

    def _hasExcludeTag(self, notes: str, comments: str) -> bool:
        """Check if notes or comments contain the exclusion tag."""
        searchText = (notes + " " + comments).lower()
        return self.EXCLUDE_TAG in searchText

    def getProfileList(self) -> List[str]:
        """Returns list of all profile names."""
        profilesPath = self._strings.moProfilesPath
        try:
            return [p for p in os.listdir(profilesPath)
                    if Path(profilesPath, p).is_dir()]
        except OSError as e:
            self._log.warning(f"Could not read profiles directory: {e}")
            return []

    def getProfileModlist(self, profileName: str) -> Tuple[Dict[str, bool], List[str]]:
        """
        Returns tuple of ({mod_name: is_enabled}, [mod_names_in_ui_order]) for a profile.
        Reads from modlist.txt where + = enabled, - = disabled.
        Note: modlist.txt is in reverse order from MO2 UI, so we reverse it.
        """
        modlistPath = self._strings.profileModlistPath(profileName)
        lines = loadLines(modlistPath)
        if lines is None:
            self._log.warning(f"Could not read modlist for {profileName}")
            return {}, []

        result = {}
        order = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("+"):
                modName = line[1:]
                result[modName] = True
                order.append(modName)
            elif line.startswith("-"):
                modName = line[1:]
                result[modName] = False
                order.append(modName)

        # Reverse to match MO2 UI order (file is stored in reverse)
        order.reverse()
        return result, order

    def readMetaIni(self, modName: str) -> Dict[str, str]:
        """
        Reads meta.ini for a mod and returns relevant fields.
        Returns dict with keys: notes, comments, gameName, modid
        """
        metaPath = self._strings.modMetaPath(modName)
        result = {"notes": "", "comments": "", "gameName": "", "modid": ""}

        if not Path(metaPath).exists():
            return result

        try:
            config = configparser.ConfigParser()
            config.read(metaPath, encoding="utf-8-sig")

            if config.has_section("General"):
                if config.has_option("General", "notes"):
                    result["notes"] = config.get("General", "notes", fallback="")
                if config.has_option("General", "comments"):
                    result["comments"] = config.get("General", "comments", fallback="")
                if config.has_option("General", "gameName"):
                    result["gameName"] = config.get("General", "gameName", fallback="")
                if config.has_option("General", "modid"):
                    result["modid"] = config.get("General", "modid", fallback="")
        except Exception as e:
            self._log.warning(f"Error reading meta.ini for {modName}: {e}")

        return result

    def collectModData(self, profileNames: List[str]) -> Tuple[List[ModInfo], List[str]]:
        """
        Collects mod data for all mods enabled in at least one selected profile.

        Returns:
            Tuple of (list of ModInfo, list of category names in order)
        """
        if not profileNames:
            return [], []

        # Get combined modlist with enabled states per profile
        allMods = {}  # {mod_name: {profile: enabled}}
        modOrder = []  # Preserve order from first profile (in UI order)

        for profileName in profileNames:
            profileMods, profileOrder = self.getProfileModlist(profileName)
            # Use order from first profile
            if not modOrder:
                modOrder = profileOrder
            for modName, enabled in profileMods.items():
                if modName not in allMods:
                    allMods[modName] = {}
                allMods[modName][profileName] = enabled

        # Filter to only mods enabled in at least one profile
        enabledMods = {
            name: profiles
            for name, profiles in allMods.items()
            if any(profiles.values())
        }

        # Build category mapping from separators
        # In UI order: separator comes BEFORE mods in that category
        categories = {}  # {mod_name: category_name}
        categoryOrder = []  # Categories in order they appear
        currentCategory = ""

        for modName in modOrder:
            if modName.endswith("_separator"):
                currentCategory = modName.replace("_separator", "")
                if currentCategory not in categoryOrder:
                    categoryOrder.append(currentCategory)
            else:
                categories[modName] = currentCategory

        # Build ModInfo list
        result = []
        excludedCount = 0
        for modName in modOrder:
            if modName.endswith("_separator"):
                continue  # Skip separator entries
            if modName not in enabledMods:
                continue  # Skip mods not enabled in any selected profile

            meta = self.readMetaIni(modName)

            # Check for exclusion tag
            if self._hasExcludeTag(meta["notes"], meta["comments"]):
                self._log.debug(f"Excluding mod '{modName}' due to <LE_Exclude> tag")
                excludedCount += 1
                continue

            # Parse nexus ID
            nexusId = None
            try:
                if meta["modid"]:
                    nexusId = int(meta["modid"])
            except ValueError:
                pass

            modInfo = ModInfo(
                name=modName,
                category=categories.get(modName, ""),
                notes=meta["notes"],
                comments=meta["comments"],
                game_name=meta["gameName"] if meta["gameName"] else None,
                nexus_id=nexusId,
                enabled_profiles={
                    p: enabledMods[modName].get(p, False)
                    for p in profileNames
                }
            )
            result.append(modInfo)

        if excludedCount > 0:
            self._log.info(f"Excluded {excludedCount} mod(s) due to <LE_Exclude> tag")

        # Filter categoryOrder to only include categories with mods
        usedCategories = set(m.category for m in result if m.category)
        categoryOrder = [c for c in categoryOrder if c in usedCategories]

        return result, categoryOrder
