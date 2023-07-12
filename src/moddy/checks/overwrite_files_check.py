import mobase, os, shutil, subprocess

from os import listdir
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

class OverwriteFilesCheck(ModdyCheck):

    def __init__(self, organiser=mobase.IOrganizer):
        super().__init__(organiser)

    def identifier(self):
        return "OverwriteFiles"
    
    def name(self):
        return "Files in Overwrite"
    
    def description(self):
        return "There are files in your overwrite folder."
    
    def shortDescription(self):
        return "There are files in your overwrite folder."

    def message(self):
        return "There are files in your overwrite folder. Would you like to view the files, make a mod from them or delete them?"

    def level(self):
        return 2

    def hasResolution(self):
        return True

    def check(self):
        qInfo("Checking for files in the overwrite folder.")
        overwriteDir = self.organiser.overwritePath()
        overwriteFiles = listdir(overwriteDir)
        return len(overwriteFiles) > 0
    
    def resolveView(self):
        qInfo("Opening the overwrite folder.")
        tkExe = "explorer.exe"
        overwritePath = str(self.organiser.overwritePath()).replace("/", "\\")
        viewFiles = f'"{tkExe}" "{overwritePath}"'
        qInfo("Executing command " + str(viewFiles))
        subprocess.call(viewFiles, shell=True, stdout=open(os.devnull, 'wb'))
        
    def resolveDelete(self):
        qInfo("Clearing the overwrite folder.")
        self.deleteOverwriteContents()
        self.dialog.hide()
        
    def resolveCreate(self):
        qInfo("Creating a mod from the overwrite folder.")
        modName = self.createModDdl.currentText()
        modDir = self.organiser.modsPath()
        newModPath = Path(modDir).joinpath(str(modName))
        if not newModPath.exists():
            os.mkdir(newModPath)
        shutil.copytree(str(self.organiser.overwritePath()), str(newModPath), dirs_exist_ok = True)
        self.organiser.refresh(True)
        self.deleteOverwriteContents()
        self.dialog.hide()

    def deleteOverwriteContents(self):
        overwriteDir = self.organiser.overwritePath()
        for file in listdir(overwriteDir):
            file_path = os.path.join(overwriteDir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                qInfo("Could not delete: " + file_path)

    def getResolveWidget(self, dialog=QDialog):
        self.overwriteActions = self.actionWidget(dialog)

        self.viewFilesBtn = self.actionButton(self.overwriteActions)
        self.viewFilesBtn.setGeometry(self.posTopLeft())
        self.viewFilesBtn.setObjectName("viewFilesBtn")
        self.viewFilesBtn.setText("View Files")
        self.viewFilesBtn.clicked.connect(self.resolveView)

        self.deleteFilesBtn = self.actionButton(self.overwriteActions)
        self.deleteFilesBtn.setGeometry(self.posTopRight())
        self.deleteFilesBtn.setObjectName("deleteFilesBtn")
        self.deleteFilesBtn.setText("Delete Files")
        self.deleteFilesBtn.clicked.connect(self.resolveDelete)

        self.createModDdl = self.actionComboBox(self.overwriteActions)
        self.createModDdl.setGeometry(self.posBtmLeft())
        self.createModDdl.setObjectName("createModDdl")
        self.createModDdl.setEditable(True)
        self.createModDdl.addItem("Overwrite Files")
        for mod in self.organiser.modList().allMods():
            if mod != "Overwrite Files":
                self.createModDdl.addItem(mod)
        
        self.createModBtn = self.actionButton(self.overwriteActions)
        self.createModBtn.setGeometry(self.posBtmRight())
        self.createModBtn.setObjectName("createModBtn")
        self.createModBtn.setText("Create or Merge with Mod")
        self.createModBtn.clicked.connect(self.resolveCreate)

        return self.overwriteActions
