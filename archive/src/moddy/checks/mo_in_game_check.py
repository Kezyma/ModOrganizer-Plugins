import mobase, os, subprocess

from pathlib import Path

try:
    from PyQt5.QtCore import qInfo
    from PyQt5.QtWidgets import QDialog
    from PyQt5 import QtWidgets, QtGui, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtCore import qInfo
    from PyQt6.QtWidgets import QDialog
    from PyQt6 import QtWidgets, QtGui, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy.Policy

from ..moddy_check import ModdyCheck

class MOInGameFolderCheck(ModdyCheck):

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__(organiser)

    def identifier(self):
        return "MOInGame"
    
    def name(self):
        return "Mod Organizer in Game Folder"
    
    def description(self):
        return "Mod Organizer is installed in the game folder and Root Builder is currently enabled."
    
    def shortDescription(self):
        return "Mod Organizer is installed in the game folder and Root Builder is currently enabled."
    
    def message(self):
        return "Mod Organizer is installed inside the game folder. This is not supported with Root Builder and will cause problems running the game! Please exit and move Mod Organizer, or disable Root Builder."

    def level(self):
        return 3

    def hasResolution(self):
        return True
    
    def check(self):
        qInfo("Checking for MO in the game folder.")
        rootBuilderPath = Path(__file__).parent.parent.parent.parent.joinpath("plugins").joinpath("rootbuilder")
        if rootBuilderPath.exists():
            modOrganizerPath = Path(__file__).parent.parent.parent.parent
            gamePath = Path(self.organiser.managedGame().gameDirectory().path())
            if gamePath in modOrganizerPath.parents:
                return True
        return False
    
    def resolveClose(self):
        qInfo("Exiting Mod Organizer.")
        tkExe = "C:/Windows/system32/taskkill.exe"
        moKill = f'"{tkExe}" /IM ModOrganizer.exe'
        qInfo("Executing command " + str(moKill))
        subprocess.call(moKill, shell=True, stdout=open(os.devnull, 'wb'))

    def resolveDisableRb(self):
        qInfo("Disabling Root Builder.")
        self.organiser.setPluginSetting("RootBuilder", "enabled", False)
        self.dialog.hide()

    def getResolveWidget(self, dialog=QDialog):
        self.overwriteActions = self.actionWidget(dialog)

        self.closeMoBtn = self.actionButton(self.overwriteActions)
        self.closeMoBtn.setGeometry(self.posTopLeft())
        self.closeMoBtn.setObjectName("closeMoBtn")
        self.closeMoBtn.setText("Exit Mod Organizer")
        self.closeMoBtn.clicked.connect(self.resolveClose)
        
        self.disableRbBtn = self.actionButton(self.overwriteActions)
        self.disableRbBtn.setGeometry(self.posTopRight())
        self.disableRbBtn.setObjectName("disableRbBtn")
        self.disableRbBtn.setText("Disable Root Builder")
        self.disableRbBtn.clicked.connect(self.resolveDisableRb)

        return self.overwriteActions
