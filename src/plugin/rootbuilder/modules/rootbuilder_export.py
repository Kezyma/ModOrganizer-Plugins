import mobase
from pathlib import Path
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import saveJson, loadJson
from ....common.common_log import CommonLog

class RootBuilderExport:
    """Root Builder export module, used to export and import settings from files."""

    def __init__(self, organiser: mobase.IOrganizer, settings: RootBuilderSettings, log: CommonLog) -> None:
        self._organiser = organiser
        self._log = log
        self._settings = settings

    def exportSettings(self, path:str):
        """Exports the current settings to the following path"""
        rbSettings = {
            "copypriority": self._settings.copypriority(),
            "copyfiles": self._settings.copyfiles(),
            "linkpriority": self._settings.linkpriority(),
            "linkfiles": self._settings.linkfiles(),
            "usvfspriority": self._settings.usvfspriority(),
            "usvfsfiles": self._settings.usvfsfiles(),
            "backup": self._settings.backup(),
            "cache": self._settings.cache(),
            "hash": self._settings.hash(),
            "autobuild": self._settings.autobuild(),
            "redirect": self._settings.redirect(),
            "exclusions": self._settings.exclusions(),
            "installer": self._settings.installer(),
            "loglevel": self._settings.loglevel()
        }
        saveJson(path, rbSettings)

    def importSettings(self, path:str):
        """Imports settings from a path."""
        rbSettings = loadJson(path)
        if rbSettings is not None:
            self._settings.updateSetting("copypriority", rbSettings["copypriority"])
            self._settings.updateSetting("copyfiles", ",".join(rbSettings["copyfiles"]))
            self._settings.updateSetting("linkpriority", rbSettings["linkpriority"])
            self._settings.updateSetting("linkfiles", ",".join(rbSettings["linkfiles"]))
            self._settings.updateSetting("usvfspriority", rbSettings["usvfspriority"])
            self._settings.updateSetting("usvfsfiles", ",".join(rbSettings["usvfsfiles"]))
            self._settings.updateSetting("backup", rbSettings["backup"])
            self._settings.updateSetting("cache", rbSettings["cache"])
            self._settings.updateSetting("hash", rbSettings["hash"])
            self._settings.updateSetting("autobuild", rbSettings["autobuild"])
            self._settings.updateSetting("redirect", rbSettings["redirect"])
            self._settings.updateSetting("exclusions", ",".join(rbSettings["exclusions"]))
            self._settings.updateSetting("installer", rbSettings["installer"])
            self._settings.updateSetting("loglevel", rbSettings["loglevel"])

    def resetSettings(self):
        """Resets to default settings."""
        defaultsFile = Path(__file__).parent.parent / "data" / "rootbuilder_defaults.json"
        self.importSettings(str(defaultsFile.absolute()))
