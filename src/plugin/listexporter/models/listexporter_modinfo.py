from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class ModInfo:
    """Data class representing a mod's exportable information."""
    name: str
    category: str
    notes: str
    comments: str
    game_name: Optional[str]
    nexus_id: Optional[int]
    enabled_profiles: Dict[str, bool]  # {profile_name: is_enabled}

    def nexus_url(self, nexus_game: str) -> Optional[str]:
        """Returns NexusMods URL if nexus_id is available."""
        if self.nexus_id and self.nexus_id > 0 and nexus_game:
            return f"https://www.nexusmods.com/{nexus_game.lower()}/mods/{self.nexus_id}"
        return None
