import mobase
from ....base.base_settings import BaseSettings


class ListExporterSettings(BaseSettings):
    """List Exporter settings module. Used to load various plugin settings."""

    def __init__(self, organiser: mobase.IOrganizer):
        super().__init__("ListExporter", organiser)

    def defaultformat(self) -> str:
        """Default export format."""
        return self._setting("defaultformat")

    def separatecategories(self) -> bool:
        """Whether to generate separate tables per category."""
        return self._setting("separatecategories")

    def lastexportpath(self) -> str:
        """Last used export path."""
        return self._setting("lastexportpath")
