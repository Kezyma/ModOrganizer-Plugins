from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QInputDialog, QLineEdit, QWidget
from PyQt5.QtCore import QCoreApplication, qInfo, QSize
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileIconProvider
from ..pluginfinder_plugin import PluginFinderPlugin
import mobase, webbrowser

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
        return self.icons.pluginIcon()
        
    def description(self):
        return self.__tr("Opens the Plugin Finder manager.")

    def display(self):
        self.pluginfinder.deploy()
        directory = self.pluginfinder.directory()
        for plugin in directory:
            qInfo(str(plugin))
        self.dialog.show()
        self.refreshItems()

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        self.setupUi(dialog)
        return dialog
    
    def setupUi(self, widget):
        widget.setObjectName("PluginFinder")
        widget.setWindowTitle("Plugin Finder")
        widget.resize(567, 477)
        self.scrollArea = QtWidgets.QScrollArea(widget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 567, 477))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 564, 474))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def installPlugin(id=str):
        return True

    def updatePlugin(id=str):
        return True

    def uninstallPlugin(id=str):
        return True

    def refreshItems(self):
        listWidget = QtWidgets.QWidget()
        for plugin in self.pluginfinder.directory():
            row = self.getPluginWidget(plugin, listWidget)
        self.scrollArea.setWidget(listWidget)

    def getPluginWidget(self, pluginJson, listWidget):
        pluginWidget = QtWidgets.QWidget(listWidget)
        pluginWidget.setObjectName(pluginJson["Id"] + "_widget")
        pluginWidget.resize(563, 70)

        pluginNameLabel = QtWidgets.QLabel(pluginWidget)
        pluginNameLabel.setGeometry(QtCore.QRect(5, 5, 426, 21))
        pluginNameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        pluginNameLabel.setObjectName("pluginNameLabel")
        pluginNameLabel.setText("<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">" + str(pluginJson["Name"]) + "</span></p></body></html>")

        pluginDescLabel = QtWidgets.QLabel(pluginWidget)
        pluginDescLabel.setGeometry(QtCore.QRect(5, 40, 556, 31))
        pluginDescLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        pluginDescLabel.setWordWrap(True)
        pluginDescLabel.setObjectName("pluginDescLabel")
        pluginDescLabel.setText(str(pluginJson["Description"]))
        
        authorLabel = QtWidgets.QLabel(pluginWidget)
        authorLabel.setGeometry(QtCore.QRect(5, 25, 431, 16))
        authorLabel.setObjectName("authorLabel")
        authorLabel.setText("<html><head/><body><p><span style=\" font-style:italic;\">by " + str(pluginJson["Author"]) + "</span></p></body></html>")
        
        nexusButton = QtWidgets.QPushButton(pluginWidget)
        nexusButton.setGeometry(QtCore.QRect(535, 0, 26, 26))
        nexusButton.setText("")
        nexusButton.setIcon(self.icons.nexusIcon())
        nexusButton.setObjectName("nexusButton")
        nexusButton.clicked.connect(lambda: webbrowser.open(str(pluginJson["Nexus"])))
        nexusButton.setToolTip("View on Nexus Mods")
        
        githubButton = QtWidgets.QPushButton(pluginWidget)
        githubButton.setGeometry(QtCore.QRect(510, 0, 26, 26))
        githubButton.setText("")
        githubButton.setIcon(self.icons.githubIcon())
        githubButton.setObjectName("githubButton")
        githubButton.clicked.connect(lambda: webbrowser.open(str(pluginJson["Github"])))
        githubButton.setToolTip("View on Github")

        installButton = QtWidgets.QPushButton(pluginWidget)
        installButton.setGeometry(QtCore.QRect(435, 0, 26, 26))
        installButton.setText("")
        installButton.setIcon(self.icons.installIcon())
        installButton.setObjectName("installButton")
        installButton.clicked.connect(lambda: self.installPlugin(str(pluginJson["Id"])))
        installButton.setToolTip("Install this plugin.")
        
        updateButton = QtWidgets.QPushButton(pluginWidget)
        updateButton.setGeometry(QtCore.QRect(460, 0, 26, 26))
        updateButton.setText("")
        updateButton.setIcon(self.icons.syncIcon())
        updateButton.setObjectName("updateButton")
        updateButton.setToolTip("Update this plugin.")
        updateButton.clicked.connect(lambda: self.updatePlugin(str(pluginJson["Id"])))

        uninstallButton = QtWidgets.QPushButton(pluginWidget)
        uninstallButton.setGeometry(QtCore.QRect(485, 0, 26, 26))
        uninstallButton.setText("")
        uninstallButton.setIcon(self.icons.minusIcon())
        uninstallButton.setObjectName("uninstallButton")
        uninstallButton.clicked.connect(lambda: self.uninstallPlugin(str(pluginJson["Id"])))
        uninstallButton.setToolTip("Uninstall this plugin.")
        
        line = QtWidgets.QFrame(pluginWidget)
        line.setGeometry(QtCore.QRect(0, 65, 566, 10))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        
        QtCore.QMetaObject.connectSlotsByName(pluginWidget)

        return pluginWidget
