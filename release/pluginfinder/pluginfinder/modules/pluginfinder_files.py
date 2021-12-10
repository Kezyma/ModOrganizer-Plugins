import mobase
from ...shared.shared_files import SharedFiles

class PluginFinderFiles(SharedFiles):
    """ Plugin Finder file module. Used to get collections of files from different game paths. """

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__("PluginFinder", organiser) 