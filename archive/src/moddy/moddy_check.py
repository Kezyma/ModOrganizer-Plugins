import mobase

try:
    from PyQt5.QtWidgets import QDialog
    from PyQt5 import QtWidgets, QtGui, QtCore
except:
    from PyQt6.QtWidgets import QDialog
    from PyQt6 import QtWidgets, QtGui, QtCore

from .moddy_dialog import ModdyDialog

class ModdyCheck:

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser

    def identifier(self):
        return "CheckId"
    
    def name(self):
        return "Check Name"
    
    def description(self):
        return "Description of what this check does."
    
    def shortDescription(self):
        return "Shorter description of what this check does."
    
    def message(self):
        return "The message that Moddy will give to the user if this check fails."
    
    def hasResolution(self):
        return False

    def level(self):
        # 3 = Critical Problem
        # 2 = Potential Issue
        # 1 = General Suggestion
        return 1

    def check(self):
        # Return true if the check fails. False otherwise.
        return False
    
    def stop(self):
        # Binds to the "don't show again" button.
        currentStops = self.organiser.pluginSetting("Moddy", "disabledchecks")
        stopArray = currentStops.split("|")
        stopArray.append(self.identifier())
        newStops = "|".join(stopArray)
        self.organiser.setPluginSetting("Moddy", "disabledchecks", newStops)
        self.dialog.hide()
        
    def resolve(self, dialog=ModdyDialog):
        self.dialog = dialog
        dialog.setMessage(self.message())
        widget = self.getResolveWidget(dialog.dialog)
        if widget:
            dialog.addOptions(widget)
        dialog.stopBtn.clicked.disconnect()
        dialog.stopBtn.clicked.connect(self.stop)
        dialog.show()

    def getActions(self, dialog=QDialog):
        # Return a QWidget containing buttons for the various different options.
        return None
    
    def actionWidget(self, dialog=QDialog):
        self.resolveWidget = QtWidgets.QWidget(dialog)
        self.resolveWidget.setObjectName("resolveWidget")
        self.resolveWidget.resize(611, 111)
        return self.resolveWidget
    
    def actionButton(self, widget=QtWidgets.QWidget):
        newBtn = QtWidgets.QPushButton(widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        newBtn.setFont(font)
        return newBtn
    
    def actionText(self, widget=QtWidgets.QWidget):
        newTxt = QtWidgets.QLineEdit(widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        newTxt.setFont(font)
        return newTxt
    
    def actionComboBox(self, widget=QtWidgets.QWidget):
        newDdl = QtWidgets.QComboBox(widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        newDdl.setFont(font)
        return newDdl

    def posTopLeft(self):
        return QtCore.QRect(10, 10, 231, 41)
    
    def posTopRight(self):
        return QtCore.QRect(250, 10, 231, 41)
    
    def posBtmLeft(self):
        return QtCore.QRect(10, 60, 231, 41)
    
    def posBtmRight(self):
        return QtCore.QRect(250, 60, 231, 41)