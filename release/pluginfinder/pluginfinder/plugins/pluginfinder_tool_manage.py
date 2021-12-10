from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
from PyQt5.QtCore import QCoreApplication, qInfo, QSize
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileIconProvider
from ..pluginfinder_plugin import PluginFinderPlugin
import mobase

class PluginFinderManageTool(PluginFinderPlugin, mobase.IPluginTool):
    
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.dialog = self.getDialog()
        return super().init(organiser)

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.menuIcon()
        
    def description(self):
        return self.__tr("Opens the Plugin Finder manager.")

    def display(self):
        self.pluginfinder.initialDeploy()
        self.dialog.show()

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        self.setupUi(dialog)
        return dialog
    
    def setupUi(self, widget):
        widget.setObjectName("PluginFinder")
        widget.resize(400, 215)
        widget.setWindowTitle("Plugin Finder")
        QtCore.QMetaObject.connectSlotsByName(widget)