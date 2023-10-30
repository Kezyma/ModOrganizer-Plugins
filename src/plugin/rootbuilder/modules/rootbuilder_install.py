import mobase
from pathlib import Path
from .rootbuilder_strings import RootBuilderStrings
from .rootbuilder_paths import RootBuilderPaths
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog
from ....common.common_qt import *
try:
    from ..ui.qt6.rootbuilder_install import Ui_installDialogMenu
except:
    from ..ui.qt5.rootbuilder_install import Ui_installDialogMenu

class RootBuilderInstall(QtWidgets.QWidget):
    """Root Builder install module, used to check and install Root mods automatically."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, strings:RootBuilderStrings, paths:RootBuilderPaths, utilities:CommonUtilities, log:CommonLog):
        super().__init__(parent)
        self._organiser = organiser
        self._strings = strings
        self._util = utilities
        self._log = log
        self._paths = paths
        self.generateLayout()

    _rootKey = "RootMaps"
    _dataKey = "DataMaps"
    _rootExtKey = "RootExt"
    _dataExtKey = "DataExt"
    _inalidKey = "InvalidMaps"
    _ignoreKey = "IgnoreMaps"
    _maps = None
    _tree = None
    _root = None

    def generateLayout(self):
        """Generates the install widget."""
        self.widget = Ui_installDialogMenu()
        self.widget.setupUi(self)

    def maps(self) -> dict:
        """Gets the current maps."""
        if self._maps == None:
            mapPath = Path(__file__).parent.parent / "data" / "rootbuilder_maps.json"
            self._maps = self._util.loadJson(str(mapPath.absolute()))
        return self._maps

    def isRootMod(self, tree: mobase.IFileTree) -> bool:
        """Determines if an IFileTree represents a likely root mod."""
        maps = self.maps()

        # Has this mod got any of the custom Root mod maps in here? If so, it's a Root mod.
        customMaps = maps[self._rootKey]
        for cm in customMaps:
            self._log.debug("Searching for " + cm)
            dataItm = tree.find(cm)
            if dataItm:
                self._log.debug("Found " + dataItm.name())
                return True
            
        # Has this mod been explicitly ignored (eg. FOMOD mods), if so, it's not a Root mod.
        ignoreMaps = maps[self._ignoreKey]
        for im in ignoreMaps:
            self._log.debug("Searching for " + im)
            dataItm = tree.find(im)
            if dataItm:
                self._log.debug("Found " + dataItm.name())
                return False

        # Does the top level of this mod contain a Data folder item? if so, it's not a Root mod.
        dataMaps = maps[self._dataKey]
        for dm in dataMaps:
            self._log.debug("Searching for " + dm)
            dataItm = tree.find(dm)
            if dataItm:
                self._log.debug("Found " + dataItm.name())
                return False
            
        # Does the top level of this mod contain a Data folder file? if so, it's not a Root mod.
        #self._foundDataExt = False
        #tree.walk(self.hasDataExt)
        #if self._foundDataExt:
        #    return False
            
        # Has this mod got any sepcifically Root files in here? If so, it's a Root mod.
        self._foundRootExt = False
        tree.walk(self.hasRootExt)
        if self._foundRootExt:
            return True
        
        # Looks like it doesn't match anything, so skip it.
        return False

    def repackMod(self, tree: mobase.IFileTree):
        """Repacks a data folder for install."""
        gameDataDir = self._strings.gameDataPath()
        gameDir = self._strings.gamePath()
        dataIsSubdir = self._paths.pathShared(gameDir, gameDataDir)
        dataFolder = self._strings.gameDataFolder()
        if not dataIsSubdir:
            dataFolder = "Data"
        maps = self.maps()
        self._tree = tree

        rootLevel = None
        dataLevel = None

        # If Data is a subdir of the game, search for it.
        if dataIsSubdir:
            dataItm = tree.find(dataFolder)
            if dataItm:
                dataLevel = dataItm
        # If Data wasn't found, search for the appropriate place.
        if dataLevel == None:
            self._dataPath = None
            tree.walk(self.findDataPath)
            if self._dataPath != None:
                dataLevel = self._dataPath
        # If there is no data, create a data path.
        if dataLevel == None:
            dataLevel = tree.addDirectory(dataFolder)

        # If there's a custom map, the data level is there.
        customMaps = maps[self._rootKey]
        for cm in customMaps:
            dataItm = tree.find(cm)
            if dataItm:
                rootLevel = dataItm
        # If there's no custom map, look for the root files.
        if rootLevel == None:
            self._rootPath = None
            tree.walk(self.findRootPath)
            if self._rootPath != None:
                rootLevel = self._rootPath
        # Detach any root invalid files.
        rootLevel.walk(self.detachInvalid)

        self._root = dataLevel.addDirectory("Root")
        rootLevel.walk(self.moveToRoot)

        return dataLevel

    _foundDataExt = False
    def hasDataExt(self, path:str, entry:mobase.FileTreeEntry) -> mobase.IFileTree.WalkReturn:
        """Checks if an entry is data folder item and skips it if so."""
        for ft in self.maps()[self._dataExtKey]:
            self._log.debug("Checking for extension " + ft)
            if entry.name().lower().endswith("." + ft):
                self._log.debug("Found " + entry.name())
                self._foundDataExt = True
                return mobase.IFileTree.STOP
        return mobase.IFileTree.CONTINUE
    
    _foundRootExt = False
    def hasRootExt(self, path:str, entry:mobase.FileTreeEntry) -> mobase.IFileTree.WalkReturn:
        """Checks if an entry is Root folder item and skips it if so."""
        for ft in self.maps()[self._rootExtKey]:
            self._log.debug("Checking for extension " + ft)
            if entry.name().lower().endswith("." + ft):
                self._log.debug("Found " + entry.name())
                self._foundRootExt = True
                return mobase.IFileTree.STOP
        return mobase.IFileTree.CONTINUE

    _rootPath = None
    def findRootPath(self, path:str, entry:mobase.FileTreeEntry) -> mobase.IFileTree.WalkReturn:
        """Finds the path to the Root directory in a mod."""
        for ft in self.maps()[self._rootExtKey]:
            if entry.name().lower().endswith("." + ft):
                parentItem = entry.parent()
                if parentItem == None:
                    self._rootPath = self._tree
                elif self._rootPath == None:
                    self._rootPath = parentItem
                else:
                    isHigher = self._rootPath.pathTo(parentItem) == ""
                    if isHigher:
                        self._rootPath = parentItem
                
        return mobase.IFileTree.CONTINUE

    _dataPath = None
    def findDataPath(self, path:str, entry:mobase.FileTreeEntry) -> mobase.IFileTree.WalkReturn:
        """Finds the path to the Data directory in a mod."""
        for ft in self.maps()[self._dataExtKey]:
            if entry.name().lower().endswith("." + ft):
                parentItem = entry.parent()
                if parentItem == None:
                    self._dataPath = self._tree
                else:
                    self._dataPath = parentItem
                return mobase.IFileTree.STOP
        return mobase.IFileTree.CONTINUE
    
    def detachInvalid(self, path:str, entry:mobase.FileTreeEntry) -> mobase.IFileTree.WalkReturn:
        """Detaches an entry invalid for root."""
        for ft in self.maps()[self._ignoreKey]:
            if entry.name().lower() == ft.lower():
                entry.detach()
        return mobase.IFileTree.CONTINUE

    def moveToRoot(self, path:str, entry:mobase.FileTreeEntry) -> mobase.IFileTree.WalkReturn:
        """Moves an entry to the root."""
        if (self._root.pathTo(entry) == "" and 
            self._root.pathFrom(self._tree) != entry.pathFrom(self._tree) and
            self._dataPath.pathTo(entry) == "" and 
            self._dataPath.pathFrom(self._tree) != entry.pathFrom(self._tree)):
            dest = self._root.addDirectory(path)
            entry.moveTo(dest)
        return mobase.IFileTree.CONTINUE