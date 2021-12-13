from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QFormLayout, QInputDialog, QLineEdit, QVBoxLayout, QWidget
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
        res = super().init(organiser)
        self.dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.pluginIcon()
        
    def description(self):
        return self.__tr("Opens the Plugin Finder manager.")

    def display(self):
        self.pluginfinder.deploy()
        self.dialog.show()
        self.refreshItems()
        self.bindInstalled()

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        self.setupUi(dialog)
        return dialog
    
    def setupUi(self, widget=QtWidgets.QDialog):
        widget.setObjectName("PluginFinder")
        widget.setWindowTitle("Plugin Finder")
        widget.setFixedSize(600, 600)
        widget.setWindowIcon(self.icon())

        self.layout = QVBoxLayout(widget)
        self.layout.setContentsMargins(0,0,0,0)
        widget.setLayout(self.layout)
        self.scroll = QtWidgets.QScrollArea(widget)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedSize(600, 600)
        self.layout.addWidget(self.scroll)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def installPlugin(self, pluginId=str):
        self.pluginfinder.install(pluginId)
        self.bindInstalled()
        
    def uninstallPlugin(self, pluginId=str):
        self.pluginfinder.uninstall(pluginId)
        self.bindInstalled()

    def refreshItems(self):
        self.pluginWidgets = {}
        self.pluginButtons = {}
        self.listWidget = QWidget(self.dialog)
        self.listLayout = QFormLayout(self.listWidget)
        self.listLayout.setContentsMargins(0,5,0,0) # margin just to keep the top buttons looking silly.
        self.listWidget.setLayout(self.listLayout)
        for plugin in self.pluginfinder.directory():
            self.listLayout.addWidget(self.getPluginWidget(plugin))
        self.scroll.setWidget(self.listWidget)

    def bindInstalled(self):
        for plugin in self.pluginWidgets.keys():
            widget = self.pluginWidgets[plugin]
            widget = QWidget()
            if self.pluginfinder.isInstalled(plugin):
                self.pluginButtons[plugin]["Install"].setIcon(self.icons.syncIcon())
                self.pluginButtons[plugin]["Uninstall"].setEnabled(True)
            else:
                self.pluginButtons[plugin]["Install"].setIcon(self.icons.installIcon())
                self.pluginButtons[plugin]["Uninstall"].setEnabled(False)
            if not self.pluginfinder.hasLink(plugin, "Nexus"):
                self.pluginButtons[plugin]["Nexus"].setEnabled(False)
            if not self.pluginfinder.hasLink(plugin, "Github"):
                self.pluginButtons[plugin]["Nexus"].setEnabled(False)
            
    def getPluginWidget(self, pluginJson):
        self.pluginButtons[pluginJson["Id"]] = {}
        pluginWidget = QtWidgets.QWidget()
        pluginWidget.setObjectName(pluginJson["Id"] + "_widget")
        pluginWidget.resize(570, 75)
        pluginWidget.setFixedSize(570, 75)

        pluginNameLabel = QtWidgets.QLabel(pluginWidget)
        pluginNameLabel.setGeometry(QtCore.QRect(5, 0, 426, 21))
        pluginNameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        pluginNameLabel.setObjectName("pluginNameLabel")
        pluginNameLabel.setText("<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">" + str(pluginJson["Name"]) + "</span></p></body></html>")

        pluginDescLabel = QtWidgets.QLabel(pluginWidget)
        pluginDescLabel.setGeometry(QtCore.QRect(5, 35, 556, 28))
        pluginDescLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        pluginDescLabel.setWordWrap(True)
        pluginDescLabel.setObjectName("pluginDescLabel")
        pluginDescLabel.setText(str(pluginJson["Description"]))
        
        authorLabel = QtWidgets.QLabel(pluginWidget)
        authorLabel.setGeometry(QtCore.QRect(5, 20, 431, 16))
        authorLabel.setObjectName("authorLabel")
        authorLabel.setText("<html><head/><body><p><span style=\" font-style:italic;\">by " + str(pluginJson["Author"]) + "</span></p></body></html>")
        
        nexusButton = QtWidgets.QPushButton(pluginWidget)
        nexusButton.setGeometry(QtCore.QRect(530, 0, 26, 26))
        nexusButton.setText("")
        nexusButton.setIcon(self.icons.nexusIcon())
        nexusButton.setIconSize(QtCore.QSize(16,16))
        nexusButton.setObjectName("nexusButton")
        nexusButton.clicked.connect(lambda: webbrowser.open(str(pluginJson["Nexus"])))
        nexusButton.setToolTip("View on Nexus Mods")
        self.pluginButtons[pluginJson["Id"]]["Nexus"] = nexusButton
        
        githubButton = QtWidgets.QPushButton(pluginWidget)
        githubButton.setGeometry(QtCore.QRect(490, 0, 26, 26))
        githubButton.setText("")
        githubButton.setIcon(self.icons.githubIcon())
        githubButton.setIconSize(QtCore.QSize(16,16))
        githubButton.setObjectName("githubButton")
        githubButton.clicked.connect(lambda: webbrowser.open(str(pluginJson["Github"])))
        githubButton.setToolTip("View on Github")
        self.pluginButtons[pluginJson["Id"]]["Github"] = githubButton

        uninstallButton = QtWidgets.QPushButton(pluginWidget)
        uninstallButton.setGeometry(QtCore.QRect(450, 0, 26, 26))
        uninstallButton.setText("")
        uninstallButton.setIcon(self.icons.minusIcon())
        uninstallButton.setIconSize(QtCore.QSize(16,16))
        uninstallButton.setObjectName("uninstallButton")
        uninstallButton.clicked.connect(lambda: self.uninstallPlugin(str(pluginJson["Id"])))
        uninstallButton.setToolTip("Uninstall this plugin.")
        self.pluginButtons[pluginJson["Id"]]["Uninstall"] = uninstallButton
        
        installButton = QtWidgets.QPushButton(pluginWidget)
        installButton.setGeometry(QtCore.QRect(410, 0, 26, 26))
        installButton.setText("")
        installButton.setIcon(self.icons.installIcon())
        installButton.setIconSize(QtCore.QSize(16,16))
        installButton.setObjectName("installButton")
        installButton.clicked.connect(lambda: self.installPlugin(str(pluginJson["Id"])))
        installButton.setToolTip("Install this plugin.")
        self.pluginButtons[pluginJson["Id"]]["Install"] = installButton
        
        line = QtWidgets.QFrame(pluginWidget)
        line.setGeometry(QtCore.QRect(0, 65, 590, 10))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        
        QtCore.QMetaObject.connectSlotsByName(pluginWidget)

        self.pluginWidgets[pluginJson["Id"]] = pluginWidget
        return pluginWidget
