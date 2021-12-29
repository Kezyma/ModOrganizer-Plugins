try:
    from PyQt5.QtCore import QCoreApplication, qInfo
    from PyQt5.QtWidgets import QInputDialog, QLineEdit
    from PyQt5 import QtWidgets, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
    from PyQt6.QtWidgets import QInputDialog, QLineEdit
    from PyQt6 import QtWidgets, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy.Policy
from ..rootbuilder_plugin import RootBuilderPlugin
from typing import Union, Tuple
from pathlib import Path
import mobase

class RootBuilderInstallPlugin(RootBuilderPlugin, mobase.IPluginInstallerSimple):
    """ Root Builder installer plugin. Handles rearranging known mods """

    def __init__(self):
        self.dialog = self.getInstallDialog()
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        return res
    
    def description(self):
        return self.__tr("Allows automatic install for Root mods.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def master(self):
        return self.pluginName

    def settings(self):
        return []

    def name(self):
        return self.baseName() + " Installer Plugin"

    def displayName(self):
        return self.baseDisplayName() + " Installer"

    _installerPathToData = str()
    def findInstallerPathToData(self, path: str, entry: mobase.FileTreeEntry):
        if str(entry.name()).lower() == str(self.rootBuilder.paths.gameDataDir()).lower():
            self._installerPathToData = str(Path(str(entry.path())).parent)
            return mobase.IFileTree.STOP
        return mobase.IFileTree.CONTINUE

    _installerHasValidFiles = False
    def checkInstallerValidFiles(self, path: str, entry: mobase.FileTreeEntry):
        en = str(entry.name())
        if en.lower() == str(self.rootBuilder.paths.gameDataDir()).lower():
            return mobase.IFileTree.SKIP
        for f in self.excRootFiles():
            if en.lower() == f.lower():
                return mobase.IFileTree.SKIP
        for e in self.minRootTypes():
            if en.lower().endswith("." + e.lower()):
                self._installerHasValidFiles = True
                return mobase.IFileTree.STOP
        return mobase.IFileTree.CONTINUE

    _installableFiles = []
    _rootLevelPath = str()
    def findInstallableFiles(self, path: str, entry: mobase.FileTreeEntry): 
        en = str(entry.name())
        if Path(path) == Path(self._rootLevelPath):
            if en.lower() == str(self.rootBuilder.paths.gameDataDir()).lower():
                return mobase.IFileTree.SKIP
            for f in self.excRootFiles():
                if en.lower() == f.lower():
                    return mobase.IFileTree.SKIP
            self._installableFiles.append(entry)
            return mobase.IFileTree.SKIP
        return mobase.IFileTree.CONTINUE

    _installerValidFilePath = str()
    _sameLevelPaths = False
    _first = True
    def findInstallerValidPath(self, path: str, entry: mobase.FileTreeEntry): 
        en = str(entry.name())
        if en.lower() == str(self.rootBuilder.paths.gameDataDir()).lower():
            return mobase.IFileTree.SKIP
        for f in self.excRootFiles():
            if en.lower() == f.lower():
                return mobase.IFileTree.SKIP
        for e in self.minRootTypes():
            if en.lower().endswith("." + e.lower()):
                p = str(path)
                qInfo("Path: " + p)
                qInfo("Curr: " + self._installerValidFilePath)
                pl = len(p.split("\\"))
                cl = len(self._installerValidFilePath.split("\\"))
                qInfo("PL:" + str(pl) + "CL:" + str(cl))
                if p != self._installerValidFilePath:
                    if not self._first and pl == cl:
                        self._sameLevelPaths = True
                    if self._first or pl < cl:
                        self._installerValidFilePath = p
                        self._sameLevelPaths = False
                        self._first = False
                return mobase.IFileTree.SKIP
        return mobase.IFileTree.CONTINUE

    _hasBaseExtensions = False
    def findBaseExtensions(self, path: str, entry: mobase.FileTreeEntry):
        for f in self.dataDirExtensions():
            if entry.name().lower().endswith("." + f):
                self._hasBaseExtensions = True
        return mobase.IFileTree.SKIP

    def isArchiveSupported(self, tree: mobase.IFileTree) -> bool: #required
        if not self.rootBuilder.settings.installer():
            return False

        for f in self.dataDirPaths():
            ft = tree.find(f)
            if ft:
                return False

        # Search for a 'known' folder, if it exists, this is almost certainly a root mod.
        for f in self.knownRootFiles():
            ft = tree.find(f)
            if ft:
                return True
            
        # Search for a Data folder. if there is one, this path to this folder is the Root path, otherwise the base itself is the root path.
        self._installerPathToData = str()
        tree.walk(self.findInstallerPathToData)
        rootTree = tree
        if self._installerPathToData != str():
            rootTree = tree.find(self._installerPathToData)
        else:
            # Check if the top level contains data dir content, return false if it does.
            for f in self.dataDirPaths():
                if rootTree.find(f):
                    return False
            self._hasBaseExtensions = False
            rootTree.walk(self.findBaseExtensions)
            if self._hasBaseExtensions:
                return False
        
        if rootTree:
            # Check the Data folder path, minus the data folder and any exclusions. If a valid file type exists anywhere in the tree, it's probably a root mod.
            self._installerHasValidFiles = False
            rootTree.walk(self.checkInstallerValidFiles)
            if self._installerHasValidFiles:
                self._first = True
                tree.walk(self.findInstallerValidPath)
                if not self._sameLevelPaths:
                    return True
                
        return False

    def isManualInstaller(self) -> bool: #required
        return False

    def priority(self) -> int: #required
        return self.rootBuilder.settings.priority()

    def install(self, name: mobase.GuessedString, tree: mobase.IFileTree, version: str, nexus_id: int) -> Union[mobase.InstallResult, mobase.IFileTree, Tuple[mobase.InstallResult, mobase.IFileTree, str, int]]:
        qInfo(str(name))
        qInfo(str(name.variants()))

        self.nameCombo.clear()
        self.nameCombo.addItems(name.variants())
        res = self.dialog.exec()
        qInfo(str(res))
        if res == QtWidgets.QDialog.Rejected:
            if self._manualRequest:
                self._manualRequest = False
                return mobase.InstallResult.MANUAL_REQUESTED
            else:
                return mobase.InstallResult.CANCELED

        if res == QtWidgets.QDialog.Accepted:
            # Get the data folder for the mod. Create a Data folder at the top level otherwise.
            self._installerPathToData = str()
            tree.walk(self.findInstallerPathToData)
            dataTree = tree
            dataPath = ""
            if self._installerPathToData != str():
                qInfo("Found data folder.")
                dataTree = tree.find(str(Path(self._installerPathToData) / self.rootBuilder.paths.gameDataDir()))
            else:
                dataTree = tree.addDirectory(self.rootBuilder.paths.gameDataDir())
            dataPath = str(dataTree.path())
            qInfo("Data path location: " + str(dataPath))

            # Find the root level folder in the mod.
            rootLevel = None

            # If it's a known mod, just use the map to save time.
            for f in self.knownRootFiles():
                qInfo("Checking for known file: " + str(f))
                ft = tree.find(f)
                if ft:
                    qInfo("Found known file: " + str(f))
                    rp = self.knownRootMaps()[str(f)]
                    if rp == "":
                        rootLevel = tree
                    else:
                        rootLevel = tree.find(rp)

            # If it's not known, find wherever the valid root file was and set that as the root level.
            if rootLevel == None:
                self._installerValidFilePath = str()
                self._first = True
                tree.walk(self.findInstallerValidPath)
                if self._installerValidFilePath != str():
                    rootLevel = tree.find(self._installerValidFilePath)
                else: 
                    rootLevel = tree

            self._rootLevelPath = rootLevel.path()
            qInfo("Root Level: " + str(self._rootLevelPath))

            # Find all the valid entries to copy across.
            self._installableFiles = []
            tree.walk(self.findInstallableFiles)
            for f in self._installableFiles:
                qInfo("Moving " + f.path() + " entry " + f.name() + " to " + dataPath + "\\Root\\")
                if not tree.move(f, dataPath + "\\Root\\"):
                    qInfo("Move failed.")

            # Get the data folder as the tree and return it.
            return tree.find(dataPath)
        
        else:
            return mobase.InstallResult.CANCELED

    def knownRootFiles(self):
        return self.knownRootMaps().keys()

    def knownRootMaps(self):
        """ Key = identification path. Value = root path. """
        return {
            "WrapperVersion": "WrapperVersion",     # ENBseries
            "Mopy": "",                             # Wrye Bash
            "xLODGen": "",                          # xLODGen
            "DynDOLOD": "",
            "BethINI Standalone": ""
        }

    def minRootTypes(self):
        """ The minimum possible file types for a valid root install. At least one of these must be present outside the data folder. """
        return [
            "ini", 
            "exe",
            "dll"
            ]

    def excRootFiles(self):
        """ List of files or folders that should never be installed to root folders. """
        return [
            "src"
            ]
    
    def dataDirPaths(self):
        return [
            "meshes",
            "textures",
            "skse",
            "f4se",
            "fose",
            "nvse",
            "obse",
            "mwse",
            "icons"
            "materials",
            "scripts",
            "music",
            "sound",
            "shaders",
            "video",
            "fonts",
            "menus",
            "splash"
        ]

    def dataDirExtensions(self):
        return [
            "esp",
            "esm",
            "esl",
            "bsa",
            "ba2"
        ]

    _manualRequest = False
    def requestManual(self, dialog):
        self._manualRequest = True
        dialog.reject()

    def getInstallDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setObjectName("dialog")
        dialog.resize(400, 83)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.nameCombo = QtWidgets.QComboBox(dialog)
        self.nameCombo.setEditable(True)
        self.nameCombo.setObjectName("nameCombo")
        self.horizontalLayout.addWidget(self.nameCombo)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.manualBtn = QtWidgets.QPushButton(dialog)
        self.manualBtn.clicked.connect(lambda: self.requestManual(dialog))
        self.manualBtn.setObjectName("manualBtn")
        self.horizontalLayout_2.addWidget(self.manualBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, qtSizePolicy.Expanding, qtSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.okBtn = QtWidgets.QPushButton(dialog)
        self.okBtn.setDefault(True)
        self.okBtn.setObjectName("okBtn")
        self.okBtn.clicked.connect(dialog.accept)
        self.horizontalLayout_2.addWidget(self.okBtn)
        self.cancelBtn = QtWidgets.QPushButton(dialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.clicked.connect(dialog.reject)
        self.horizontalLayout_2.addWidget(self.cancelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label.setText("Name")
        self.manualBtn.setText("Manual")
        self.okBtn.setText("OK")
        self.cancelBtn.setText("Cancel")
        dialog.setWindowTitle("Root Builder Install")
        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog
        