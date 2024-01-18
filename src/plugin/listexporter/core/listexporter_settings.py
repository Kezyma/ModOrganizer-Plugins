import mobase
from ....base.base_settings import BaseSettings

class ListExporterSettings(BaseSettings):
    """ List Exporter settings module. Used to load various plugin settings. """

    def __init__(self, organiser:mobase.IOrganizer):
        super().__init__("ListExporter", organiser)