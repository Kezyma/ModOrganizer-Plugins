try:
    from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QFormLayout, QInputDialog, QLineEdit, QVBoxLayout, QWidget
    from PyQt5.QtCore import QCoreApplication, qInfo, QSize
    from PyQt5 import QtGui, QtWidgets, QtCore
    qtAlignLeading = QtCore.Qt.AlignLeading
    qtAlignLeft = QtCore.Qt.AlignLeft
    qtAlignTop = QtCore.Qt.AlignTop
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
except:
    from PyQt6.QtWidgets import QFileDialog, QFileIconProvider, QFormLayout, QInputDialog, QLineEdit, QVBoxLayout, QWidget
    from PyQt6.QtCore import QCoreApplication, qInfo, QSize
    from PyQt6 import QtGui, QtWidgets, QtCore
    qtAlignLeading = QtCore.Qt.AlignmentFlag.AlignLeading
    qtAlignLeft = QtCore.Qt.AlignmentFlag.AlignLeft
    qtAlignTop = QtCore.Qt.AlignmentFlag.AlignTop
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
from ..pluginfinder_plugin import PluginFinderPlugin
from ..models.plugin_data import PluginData
from ...shared.shared_utilities import SharedUtilities
import mobase, webbrowser, os, subprocess

class PluginFinderBrowser(PluginFinderPlugin, mobase.IPluginTool):
    
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.page = 1
        self.pageSize = 7
        self.hasChanged = False
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        self.utilities = SharedUtilities()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.pluginIcon()
        
    def description(self):
        return self.__tr("Opens the Plugin Finder manager.")

    def display(self):
        self.dialog.show()
        self.bindPage()

    def nextPage(self):
        self.page = self.page + 1
        self.bindPage()

    def prevPage(self):
        self.page = self.page - 1
        self.bindPage()

    def refreshPage(self):
        self.pluginfinder.search.refreshData()
        self.bindPage()

    def clearResults(self):
        while self.formLayout.count():
            child = self.formLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def bindPage(self):
        data = self.pluginfinder.search.pagedPluginData(self.searchText.text(), self.installedCheck.isChecked(), self.page, self.pageSize)
        self.clearResults()
        for plugin in data:
            self.formLayout.addWidget(self.getPluginWidget(plugin))
        pages = self.pluginfinder.search.totalPages(self.searchText.text(), self.installedCheck.isChecked(), self.pageSize)
        self.backButton.setEnabled(self.page != 1)
        self.nextButton.setEnabled(self.page < pages)

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        
        dialog.setWindowTitle("Plugin Finder")
        dialog.setObjectName("pluginFinder")
        dialog.resize(623, 675)
        dialog.setMinimumSize(QtCore.QSize(623, 675))
        dialog.setMaximumSize(QtCore.QSize(623, 675))
        dialog.setWindowIcon(self.icons.pluginIcon())
        dialog.rejected.connect(self.onClose)

        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setObjectName("verticalLayout")

        self.searchWidget = QtWidgets.QWidget(dialog)
        self.searchWidget.setMinimumSize(QtCore.QSize(0, 26))
        self.searchWidget.setMaximumSize(QtCore.QSize(16777215, 26))
        self.searchWidget.setObjectName("searchWidget")
        self.searchText = QtWidgets.QLineEdit(self.searchWidget)
        self.searchText.textChanged.connect(self.bindPage)
        self.searchText.setGeometry(QtCore.QRect(0, 0, 526, 21))
        self.searchText.setObjectName("searchText")
        self.searchText.setPlaceholderText("Search")
        self.installedCheck = QtWidgets.QCheckBox(self.searchWidget)
        self.installedCheck.setGeometry(QtCore.QRect(535, 0, 66, 21))
        self.installedCheck.setObjectName("installedCheck")
        self.installedCheck.setText("Installed")
        self.installedCheck.stateChanged.connect(self.bindPage)
        self.dialogLayout.addWidget(self.searchWidget)

        self.resultsWidget = QtWidgets.QWidget(dialog)
        self.resultsWidget.setObjectName("resultsWidget")
        self.formLayout = QtWidgets.QFormLayout(self.resultsWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.dialogLayout.addWidget(self.resultsWidget)

        self.pagingWidget = QtWidgets.QWidget(dialog)
        self.pagingWidget.setMinimumSize(QtCore.QSize(0, 25))
        self.pagingWidget.setMaximumSize(QtCore.QSize(16777215, 25))
        self.pagingWidget.setObjectName("pagingWidget")
        self.refreshButton = QtWidgets.QPushButton(self.pagingWidget)
        self.refreshButton.setGeometry(QtCore.QRect(277, 0, 46, 26))
        self.refreshButton.setText("")
        self.refreshButton.setIcon(self.icons.refreshIcon())
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.setToolTip("Refresh Data")
        self.refreshButton.clicked.connect(self.refreshPage)
        self.backButton = QtWidgets.QPushButton(self.pagingWidget)
        self.backButton.setGeometry(QtCore.QRect(0, 0, 46, 26))
        self.backButton.setText("")
        self.backButton.setIcon(self.icons.prevIcon())
        self.backButton.setObjectName("backButton")
        self.backButton.setToolTip("Previous Page")
        self.backButton.clicked.connect(self.prevPage)
        self.nextButton = QtWidgets.QPushButton(self.pagingWidget)
        self.nextButton.setGeometry(QtCore.QRect(555, 0, 46, 26))
        self.nextButton.setText("")
        self.nextButton.setIcon(self.icons.nextIcon())
        self.nextButton.setCheckable(False)
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setToolTip("Next Page")
        self.nextButton.clicked.connect(self.nextPage)
        self.dialogLayout.addWidget(self.pagingWidget)

        QtCore.QMetaObject.connectSlotsByName(dialog)

        return dialog
    
    def installClick(self, pluginId=str):
        self.pluginfinder.install(pluginId)
        self.hasChanged = True
        self.bindPage()

    def uninstallClick(self, pluginId=str):
        self.pluginfinder.uninstall(pluginId)
        self.hasChanged = True
        self.bindPage()

    def onClose(self):
        if self.hasChanged:
            os.system("taskkill /F /IM ModOrganizer.exe && explorer \"" + str(self.pluginfinder.paths.modOrganizerExePath()) + "\"")

    def getPluginWidget(self, pluginData=PluginData):
        widget = QtWidgets.QWidget()
        widget.setMinimumSize(QtCore.QSize(602, 80))
        widget.setMaximumSize(QtCore.QSize(602, 80))
        widget.setObjectName("widget")
        
        pluginName = QtWidgets.QLabel(widget)
        pluginName.setGeometry(QtCore.QRect(0, 0, 331, 21))
        pluginName.setObjectName("pluginName")
        pluginName.setText("<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">" + pluginData.name() + "</span></p></body></html>")

        pluginAuthor = QtWidgets.QLabel(widget)
        pluginAuthor.setGeometry(QtCore.QRect(0, 20, 381, 16))
        pluginAuthor.setObjectName("pluginAuthor")
        pluginAuthor.setText("<html><head/><body><p><span style=\" font-size:7pt; font-style:italic;\">by " + pluginData.author() + "</span></p></body></html>")

        pluginDesc = QtWidgets.QLabel(widget)
        pluginDesc.setGeometry(QtCore.QRect(0, 35, 601, 41))
        pluginDesc.setAlignment(qtAlignLeading|qtAlignLeft|qtAlignTop)
        pluginDesc.setWordWrap(True)
        pluginDesc.setObjectName("pluginDesc")        
        pluginDesc.setText(pluginData.description())

        moVersion = self.organiser.appVersion().canonicalString()
        currentPlugin = pluginData.current(moVersion) # most recent working plugin.
        currentSupported = currentPlugin and not (currentPlugin.maxSupport() == "" or currentPlugin.minSupport() == "" or self.utilities.versionIsNewer(currentPlugin.maxSupport(), moVersion) or self.utilities.versionIsNewer(moVersion, currentPlugin.minSupport()))
        latestPlugin = pluginData.latest() # most recent overall plugin.
        installed = self.pluginfinder.installer.isInstalled(pluginData.identifier())
        installedVersion = self.pluginfinder.installer.installedVersion(pluginData.identifier())

        showUpdateIcon = False
        showUnsupportedUpdateIcon = False
        showUnsupportedInstallIcon = False
        showNotWorkingIcon = False
        showNotWorkingUpdateIcon = False
        canUpdate = False
        showVersion = False
        showNoDownloadIcon = False

        displayVersion = ""
        if latestPlugin:
            displayVersion = latestPlugin.version()
        if currentPlugin and self.utilities.versionIsNewer(installedVersion, currentPlugin.version()):
            displayVersion = currentPlugin.version()

        if not currentPlugin and not latestPlugin:
            showNoDownloadIcon = True
        elif not currentPlugin:
            showNotWorkingIcon = True
            showVersion = True
        elif installed and self.utilities.versionIsNewer(installedVersion, currentPlugin.version()):
            showVersion = True
            canUpdate = True
            if currentSupported:
                showUpdateIcon = True
            else:
                showUnsupportedUpdateIcon = True 
        elif installed and self.utilities.versionIsNewer(installedVersion, latestPlugin.version()):
            showVersion = True
            showNotWorkingUpdateIcon = True
        elif not installed:
            showVersion = True
            canUpdate = True
            if not currentSupported:
               showUnsupportedInstallIcon = True
            
        if installed:
            pluginVersion = QtWidgets.QLabel(widget)
            pluginVersion.setGeometry(QtCore.QRect(345, 15, 41, 11))
            pluginVersion.setObjectName("pluginVersion")
            pluginVersion.setToolTip("Installed Version")
            pluginVersion.setText("<html><head/><body><p><span style=\" font-size:7pt;\">v" + mobase.VersionInfo(installedVersion).canonicalString() + "</span></p></body></html>")

        if showVersion:
            pluginUpdateLabel = QtWidgets.QLabel(widget)
            pluginUpdateLabel.setGeometry(QtCore.QRect(345, 0, 41, 16))
            pluginUpdateLabel.setObjectName("pluginUpdateLabel")
            pluginUpdateLabel.setToolTip("Current Version")
            pluginUpdateLabel.setText("<html><head/><body><p><span style=\" font-size:7pt;\">v" + mobase.VersionInfo(displayVersion).canonicalString() + "</span></p></body></html>")

        statusIcon = QtWidgets.QLabel(widget)
        statusIcon.setGeometry(QtCore.QRect(325, 5, 16, 21))
        statusIcon.setText("")
        statusIcon.setObjectName("statusIcon")
        if showUpdateIcon:
            statusIcon.setPixmap(self.icons.updateIcon().pixmap(QSize(16, 16)))
            statusIcon.setToolTip("There is a new update available!")
        elif showUnsupportedUpdateIcon:
            statusIcon.setPixmap(self.icons.updateAltIcon().pixmap(QSize(16,16)))
            statusIcon.setToolTip("There is a new update available but this update has not been tested with this version of Mod Organizer and may not work correctly.")
        elif showNotWorkingIcon:
            statusIcon.setPixmap(self.icons.stopIcon().pixmap(QSize(16,16)))
            statusIcon.setToolTip("There is no version of this plugin that works with this version of Mod Organizer.")
        elif showNotWorkingUpdateIcon:
            statusIcon.setPixmap(self.icons.noUpdateIcon().pixmap(QSize(16,16)))
            statusIcon.setToolTip("There is a new update available but does not work with this version of Mod Organizer.")
        elif showUnsupportedInstallIcon:
            statusIcon.setPixmap(self.icons.warningIcon().pixmap(QSize(16,16)))
            statusIcon.setToolTip("This plugin has not been tested with this version of Mod Organizer and may not work correctly.")
        elif installed:
            statusIcon.setPixmap(self.icons.checkIcon().pixmap(QSize(16,16)))
            statusIcon.setToolTip("This plugin is up to date.")
        elif showNoDownloadIcon:
            statusIcon.setPixmap(self.icons.infoIcon().pixmap(QSize(16,16)))
            statusIcon.setToolTip("This plugin cannot be installed through Plugin Finder.")
            
        docsButton = QtWidgets.QPushButton(widget)
        docsButton.setGeometry(QtCore.QRect(480, 0, 40, 26))
        docsButton.setText("")
        docsButton.setIcon(self.icons.docsIcon())
        docsButton.setObjectName("docsButton")
        docsButton.setToolTip("Documentation")
        docsButton.clicked.connect(lambda: webbrowser.open(str(pluginData.docsUrl())))
        if pluginData.docsUrl() == "":
            docsButton.setEnabled(False)
            
        nexusButton = QtWidgets.QPushButton(widget)
        nexusButton.setGeometry(QtCore.QRect(520, 0, 40, 26))
        nexusButton.setText("")
        nexusButton.setIcon(self.icons.nexusIcon())
        nexusButton.setObjectName("nexusButton")
        nexusButton.setToolTip("Nexus")
        nexusButton.clicked.connect(lambda: webbrowser.open(str(pluginData.nexusUrl())))
        if pluginData.nexusUrl() == "":
            nexusButton.setEnabled(False)

        githubButton = QtWidgets.QPushButton(widget)
        githubButton.setGeometry(QtCore.QRect(560, 0, 40, 26))
        githubButton.setText("")
        githubButton.setIcon(self.icons.githubIcon())
        githubButton.setObjectName("githubButton")
        githubButton.setToolTip("Github")
        githubButton.clicked.connect(lambda: webbrowser.open(str(pluginData.githubUrl())))
        if pluginData.githubUrl() == "":
            githubButton.setEnabled(False)
            
        uninstallButton = QtWidgets.QPushButton(widget)
        uninstallButton.setGeometry(QtCore.QRect(430, 0, 40, 26))
        uninstallButton.setText("")
        uninstallButton.setIcon(self.icons.minusIcon())
        uninstallButton.setObjectName("uninstallButton")
        uninstallButton.setToolTip("Uninstall")
        uninstallButton.setEnabled(installed)
        uninstallButton.clicked.connect(lambda: self.uninstallClick(pluginData.identifier()))

        installButton = QtWidgets.QPushButton(widget)
        installButton.setGeometry(QtCore.QRect(390, 0, 40, 26))
        installButton.setText("")
        installButton.setIcon(self.icons.installIcon())
        installButton.setObjectName("installButton")
        installButton.setToolTip("Install/Update")
        installButton.setEnabled(canUpdate)
        installButton.clicked.connect(lambda: self.installClick(pluginData.identifier()))

        line = QtWidgets.QFrame(widget)
        line.setGeometry(QtCore.QRect(0, 70, 601, 16))
        line.setFrameShape(qtHLine)
        line.setFrameShadow(qtSunken)
        line.setObjectName("line")

        return widget
