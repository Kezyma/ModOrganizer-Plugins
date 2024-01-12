import mobase, os
from pathlib import Path
from typing import List, Dict
from ....common.common_utilities import loadJson, saveJson

class ListExporterJson:
    """List Exporter Json module, handles json export of the current modlist."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser

    def export(self, path:str):
        modList = self._organiser.modList()
        orderedMods = modList.allModsByProfilePriority()
        modExport = {}
        currentCat = ""
        for mod in orderedMods:
            if str(mod).endswith("_separator"):
                currentCat = str(mod).replace("_separator", "")
                modExport[currentCat] = []
            else:
                if modList.state(mod.encode('utf-16','surrogatepass').decode('utf-16')) & mobase.ModState.ACTIVE:
                    modItem = modList.getMod(mod)
                    nexusGame = self._organiser.getGame(modItem.gameName()).gameNexusName()
                    newMod = {
                        "Name": modItem.name(),
                        "Game": modItem.gameName(),
                        "NexusId": modItem.nexusId(),
                        "NexusGame": nexusGame,
                        "Comments": modItem.comments(),
                        "Notes": modItem.notes()
                    }
                    modExport[currentCat].append(newMod)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        saveJson(path, modExport)