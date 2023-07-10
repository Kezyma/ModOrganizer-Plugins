import mobase

from os import listdir

try:
    from PyQt5.QtCore import QCoreApplication, qInfo
    from PyQt5.QtWidgets import QDialog
    from PyQt5 import QtWidgets, QtGui, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
    from PyQt6.QtWidgets import QDialog
    from PyQt6 import QtWidgets, QtGui, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy.Policy

from ..moddy_dialog import ModdyDialog

class OverwriteFilesCheck:

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser

    def identifier(self):
        return "OverwriteFiles"
    
    def name(self):
        return "Files in Overwrite"
    
    def description(self):
        return "Checks for files in the Mod Organizer overwrite folder and offers options to deal with them."

    def level(self):
        return 2

    def check(self):
        qInfo("Checking for files in the overwrite folder.")
        overwriteDir = self.organiser.overwritePath()
        overwriteFiles = listdir(overwriteDir)
        return len(overwriteFiles) > 0
    
    def stop(self):
        currentStops = self.organiser.pluginSetting("Moddy", "disabledchecks")
        stopArray = currentStops.split("|")
        stopArray.append(self.identifier())
        newStops = "|".join(stopArray)
        self.organiser.setPluginSetting("Moddy", "disabledchecks", newStops)
        self.dialog.hide()
        
    def resolve(self, dialog=ModdyDialog):
        qInfo("Displaying overwrite files resolve dialog.")
        self.dialog = dialog
        dialog.setMessage("There are files in your overwrite folder. Would you like to view the files, make a mod from them or delete them?")
        widget = self.getResolveWidget(dialog.dialog)
        dialog.addOptions(widget)
        dialog.stopBtn.clicked.disconnect()
        dialog.stopBtn.clicked.connect(self.stop)
        dialog.show()
    
    def resolveView(self):
        qInfo("Opening the overwrite folder.")

    def resolveDelete(self):
        qInfo("Clearing the overwrite folder.")

    def resolveCreate(self):
        qInfo("Creating a mod from the overwrite folder.")

    def getResolveWidget(self, dialog=QDialog):
        self.overwriteActions = QtWidgets.QWidget(dialog)
        self.overwriteActions.setObjectName("overwriteActions")
        self.overwriteActions.resize(667, 104)
        self.viewFilesBtn = QtWidgets.QPushButton(self.overwriteActions)
        self.viewFilesBtn.setGeometry(QtCore.QRect(10, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.viewFilesBtn.setFont(font)
        self.viewFilesBtn.setObjectName("viewFilesBtn")
        self.deleteFilesBtn = QtWidgets.QPushButton(self.overwriteActions)
        self.deleteFilesBtn.setGeometry(QtCore.QRect(250, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.deleteFilesBtn.setFont(font)
        self.deleteFilesBtn.setObjectName("deleteFilesBtn")
        self.createModBtn = QtWidgets.QPushButton(self.overwriteActions)
        self.createModBtn.setGeometry(QtCore.QRect(250, 60, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.createModBtn.setFont(font)
        self.createModBtn.setObjectName("createModBtn")
        self.createModTxt = QtWidgets.QLineEdit(self.overwriteActions)
        self.createModTxt.setGeometry(QtCore.QRect(10, 60, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.createModTxt.setFont(font)
        self.createModTxt.setObjectName("createModTxt")
        #self.createModTxt.setAutoFillBackground(True)
        self.viewFilesBtn.setText("View Files")
        self.deleteFilesBtn.setText("Delete Files")
        self.createModBtn.setText("Create Mod")
        return self.overwriteActions
