from .rootbuilder_settings import RootBuilderSettings
from .rootbuilder_paths import RootBuilderPaths
from .rootbuilder_files import RootBuilderFiles
import mobase, os

class RootBuilderMapper():
    """ Root Builder mapping module. Used to generate root mappings for usvfs. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = RootBuilderSettings(self.organiser)
        self.paths = RootBuilderPaths(self.organiser)
        self.files = RootBuilderFiles(self.organiser)
        super().__init__()

    def mappings(self):
        """ Gets the mappings for the current game. """
        # We only generate mappings if we're in link mode.
        if self.settings.usvfsmode():
            if not self.paths.rootOverwritePath().exists():
                os.makedirs(self.paths.rootOverwritePath())           
            # Get the mappings for installed root mods.
            rootModList = self.files.getRootMods()
            rootMappingList = self.getRootMappingList(rootModList)
            # Configure the overwrite mapping for root files.
            overwriteMap = mobase.Mapping()
            overwriteMap.source = str(self.paths.rootOverwritePath())
            overwriteMap.destination = str(self.paths.gamePath())
            overwriteMap.isDirectory = True
            overwriteMap.createTarget = True
            rootMappingList.append(overwriteMap)
            return rootMappingList
        return []

    def getRootMappingList(self, modList):
        """ Gets root mapping configurations for a given modlist. """
        mappings = []
        for mod in modList:
            rootMapping = mobase.Mapping()
            rootMapping.source = str(self.paths.modsPath() / mod / "Root")
            rootMapping.destination = str(self.paths.gamePath())
            rootMapping.isDirectory = True
            rootMapping.createTarget = False
            mappings.append(rootMapping)
        return mappings

    def cleanup(self):
        if self.paths.rootOverwritePath().exists():
            if len(os.listdir(self.paths.rootOverwritePath())) == 0:
                os.rmdir(self.paths.rootOverwritePath())
        return