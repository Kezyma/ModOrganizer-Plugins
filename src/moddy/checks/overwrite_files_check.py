import mobase

from os import listdir

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
        return "Checks for files in the Mod Organizer overwrite folder and offers options to deal with them."
    
    def message(self):
        return "There are files in your overwrite folder. Would you like to view the files, make a mod from them or delete them?"

    def level(self):
        return 2

    def check(self):
        qInfo("Checking for files in the overwrite folder.")
        overwriteDir = self.organiser.overwritePath()
        overwriteFiles = listdir(overwriteDir)
        return len(overwriteFiles) > 0
    
    def resolveView(self):
        qInfo("Opening the overwrite folder.")

    def resolveDelete(self):
        qInfo("Clearing the overwrite folder.")

    def resolveCreate(self):
        qInfo("Creating a mod from the overwrite folder.")

    def getActions(self, dialog=QDialog):
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
        self.deleteFilesBtn.clicked.connect(self.resolveDelete())

        self.createModTxt = self.actionText(self.overwriteActions)
        self.createModTxt.setGeometry(self.posBtmLeft())
        self.createModTxt.setObjectName("createModTxt")
        
        self.createModBtn = self.actionButton(self.overwriteActions)
        self.createModBtn.setGeometry(self.posBtmLeft())
        self.createModBtn.setObjectName("createModBtn")
        self.createModBtn.setText("Create Mod")
        self.createModBtn.clicked.connect(self.resolveCreate)

        return self.overwriteActions
