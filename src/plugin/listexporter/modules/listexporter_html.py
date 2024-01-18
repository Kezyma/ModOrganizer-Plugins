import mobase, os
from pathlib import Path
from typing import List, Dict
from ....common.common_utilities import loadJson, saveJson

class ListExporterHtml:
    """List Exporter Html module, handles html export of the current modlist."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser

    def export(self, path:str):
        modList = self._organiser.modList()
        orderedMods = modList.allModsByProfilePriority()
        currentCat = ""
        table = "<!DOCTYPE html><html><head>"
        table += "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'>"
        table += "<script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js'></script>"
        table += "</head><body class='bg-secondary'><div class='container'><div class='card mt-3 mb-3'><div class='card-body p-0'>"
        table += "<table class='table table-sm table-striped mb-0 pb-0'><thead><tr><th>Category</th><th>Mod</th><th>Comments</th></tr></thead><tbody>"
        for mod in orderedMods:
            if str(mod).endswith("_separator"):
                currentCat = str(mod).replace("_separator", "")
            else:
                if modList.state(mod.encode('utf-16','surrogatepass').decode('utf-16')) & mobase.ModState.ACTIVE:
                    modItem = modList.getMod(mod)
                    nexusGame = self._organiser.getGame(modItem.gameName()).gameNexusName()

                    table += "<tr><td>" + currentCat + "</td>"
                    if modItem.nexusId() > 0:
                        table += "<td><a href='https://www.nexusmods.com/" + nexusGame.lower() + "/mods/" + str(modItem.nexusId()) + "' target='_blank'>" + modItem.name() + "</a></td>"
                    else:
                        table += "<td>" + modItem.name() + "</td>"
                    table += "<td>" + modItem.comments() + "</td>"
                    table += "</tr>"

        table += "</tbody></table></div></div></div>"
        table += "</body></html>"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(Path(path), "w", encoding="utf-8") as htmlFile:
            htmlFile.write(table)