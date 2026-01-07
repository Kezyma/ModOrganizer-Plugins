import mobase
from functools import cached_property
from pathlib import Path
from ....common.common_strings import CommonStrings


class ListExporterStrings(CommonStrings):
    """List Exporter strings module, contains paths used by List Exporter."""

    def __init__(self, plugin: str, organiser: mobase.IOrganizer):
        super().__init__(plugin, organiser)

    @cached_property
    def leDataPath(self) -> str:
        """Gets the path to List Exporter data folder."""
        instanceName = self.pathSafeString(self.moInstanceName)
        if instanceName == "":
            instanceName = "Portable"
        return str(Path(self.pluginDataPath, instanceName).absolute())

    def modMetaPath(self, modName: str) -> str:
        """Gets the path to a mod's meta.ini file."""
        return str(Path(self.moModsPath, modName, "meta.ini"))

    def profileModlistPath(self, profileName: str) -> str:
        """Gets the path to a profile's modlist.txt."""
        return str(Path(self.moProfilesPath, profileName, "modlist.txt"))
