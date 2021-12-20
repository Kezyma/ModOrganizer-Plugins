try:
    from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QFormLayout, QInputDialog, QLineEdit, QVBoxLayout, QWidget
    from PyQt5.QtCore import QCoreApplication, qInfo, QSize
    from PyQt5 import QtGui, QtWidgets, QtCore
    qtAlign = QtCore.Qt
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
    qtWindow = QtCore.Qt.Window 
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtWidgets import QFileDialog, QFileIconProvider, QFormLayout, QInputDialog, QLineEdit, QVBoxLayout, QWidget
    from PyQt6.QtCore import QCoreApplication, qInfo, QSize
    from PyQt6 import QtGui, QtWidgets, QtCore
    qtAlign = QtCore.Qt.AlignmentFlag
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
    qtWindow = QtCore.Qt.WindowType.Window 
    qtSizePolicy = QtWidgets.QSizePolicy.Policy
from datetime import datetime
from ..pluginfinder_plugin import PluginFinderPlugin
from ..models.plugin_data import PluginData
from ...shared.shared_utilities import SharedUtilities
import mobase, webbrowser, os, subprocess, threading

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

    def getTempDialog(self, text=str):
        tempDialog = QtWidgets.QDialog()
        tempDialog.resize(200, 50)
        tempDialog.setMinimumSize(QtCore.QSize(200, 50))
        tempDialog.setMaximumSize(QtCore.QSize(200, 50))
        tempDialog.setObjectName("tempDialog")
        tempDialog.setWindowTitle("Plugin Finder")
        tempDialog.setWindowIcon(self.icons.pluginIcon())
        tempLabel = QtWidgets.QLabel(tempDialog)
        tempLabel.setObjectName("tempLabel")
        tempLabel.setText(text)
        tempLabel.setGeometry(QtCore.QRect(0, 0, 200, 50))
        tempLabel.setAlignment(qtAlign.AlignHCenter | qtAlign.AlignVCenter)
        tempLabel.setVisible(True)
        tempLabel.setEnabled(True)
        QtCore.QMetaObject.connectSlotsByName(tempDialog)
        return tempDialog

    def display(self):
        self.pluginfinder.initial(self.version().canonicalString())
        self.bindPage()
        self.dialog.show()

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
        while self.resultsLayout.count():
            child = self.resultsLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def bindPage(self):
        data, pages = self.pluginfinder.search.pagedPluginData(self.searchText.text(), self.installedCheck.isChecked(), self.page, self.pageSize)
        if self.page > pages:
            self.page = pages
            if self.page < 1:
                self.page = 1
            data, pages = self.pluginfinder.search.pagedPluginData(self.searchText.text(), self.installedCheck.isChecked(), self.page, self.pageSize)

        self.clearResults()
        for plugin in data:
            self.resultsLayout.addWidget(self.getPluginWidget(plugin))
            self.resultsLayout.addWidget(self.getPluginSeparator())

        missing = 7 - len(data)
        for i in range(missing):
            self.resultsLayout.addWidget(self.getEmptyPluginWidget())
            self.resultsLayout.addWidget(self.getPluginSeparator())
            
        self.prevButton.setEnabled(self.page != 1)
        self.nextButton.setEnabled(self.page < pages)
    
    def installClick(self, pluginId=str):
        increaseCount = not self.pluginfinder.installer.isInstalled(pluginId)
        self.pluginfinder.install(pluginId)
        if increaseCount:
            self.pluginfinder.search.increaseInstallCount(pluginId)
        self.hasChanged = True
        self.bindPage()

    def uninstallClick(self, pluginId=str):
        self.pluginfinder.uninstall(pluginId)
        self.pluginfinder.search.decreaseInstallCount(pluginId)
        self.hasChanged = True
        self.bindPage()

    def onClose(self):
        if self.hasChanged:
            qInfo("Plugins changed, restarting Mod Organizer.")
            tkExe = "C:/Windows/system32/taskkill.exe"
            moExe = str(self.pluginfinder.paths.modOrganizerExePath())
            moKill = f'"{tkExe}" /F /IM ModOrganizer.exe && explorer "{moExe}"'
            qInfo("Executing command " + str(moKill))
            subprocess.call(moKill, shell=True, stdout=open(os.devnull, 'wb'))

    def getDialog(self):
        # Main Dialog
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Plugin Finder")
        dialog.setObjectName("pluginFinder")
        dialog.resize(623, 700)
        dialog.setMinimumSize(QtCore.QSize(623, 700))
        dialog.setWindowIcon(self.icons.pluginIcon())
        dialog.rejected.connect(self.onClose)
        #dialog.setWindowFlags(qtStaysOnTop)
        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setObjectName("dialogLayout")

        # Header Widget
        self.filterWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterWidget.sizePolicy().hasHeightForWidth())
        self.filterWidget.setSizePolicy(sizePolicy)
        self.filterWidget.setObjectName("filterWidget")
        self.filterLayout = QtWidgets.QHBoxLayout(self.filterWidget)
        self.filterLayout.setContentsMargins(0, 0, 0, 0)
        self.filterLayout.setObjectName("filterLayout")
        self.searchText = QtWidgets.QLineEdit(self.filterWidget)
        self.searchText.setObjectName("searchText")
        self.searchText.textChanged.connect(self.bindPage)
        self.searchText.setPlaceholderText("Search")
        self.filterLayout.addWidget(self.searchText)
        self.installedCheck = QtWidgets.QCheckBox(self.filterWidget)
        self.installedCheck.setObjectName("installedCheck")
        self.installedCheck.setText("Installed")
        self.installedCheck.stateChanged.connect(self.bindPage)
        self.filterLayout.addWidget(self.installedCheck)
        self.dialogLayout.addWidget(self.filterWidget)

        # Results Widget
        self.resultsWidget = QtWidgets.QWidget(dialog)
        self.resultsWidget.setObjectName("resultsWidget")
        self.resultsLayout = QtWidgets.QVBoxLayout(self.resultsWidget)
        self.resultsLayout.setContentsMargins(0, 0, 0, 0)
        self.resultsLayout.setObjectName("resultsLayout")
        self.dialogLayout.addWidget(self.resultsWidget)

        # Footer Widget
        self.footerWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footerWidget.sizePolicy().hasHeightForWidth())
        self.footerWidget.setSizePolicy(sizePolicy)
        self.footerWidget.setObjectName("footerWidget")
        self.footerLayout = QtWidgets.QHBoxLayout(self.footerWidget)
        self.footerLayout.setObjectName("footerLayout")
        self.footerLayout.setContentsMargins(0, 0, 0, 0)
        self.prevButton = QtWidgets.QPushButton(self.footerWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prevButton.sizePolicy().hasHeightForWidth())
        self.prevButton.setSizePolicy(sizePolicy)
        self.prevButton.setText("")
        self.prevButton.setIcon(self.icons.prevIcon())
        self.prevButton.setFlat(True)
        self.prevButton.setObjectName("prevButton")
        self.prevButton.setToolTip("Previous Page")
        self.prevButton.clicked.connect(self.prevPage)
        self.footerLayout.addWidget(self.prevButton)

        spacerItem = QtWidgets.QSpacerItem(40, 20, qtSizePolicy.Expanding, qtSizePolicy.Minimum)
        self.footerLayout.addItem(spacerItem)

        self.refreshButton = QtWidgets.QPushButton(self.footerWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setText("")
        self.refreshButton.setIcon(self.icons.refreshIcon())
        self.refreshButton.setFlat(True)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.setToolTip("Refresh Data")
        self.refreshButton.clicked.connect(self.refreshPage)
        self.footerLayout.addWidget(self.refreshButton)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, qtSizePolicy.Expanding, qtSizePolicy.Minimum)
        self.footerLayout.addItem(spacerItem1)

        self.nextButton = QtWidgets.QPushButton(self.footerWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setText("")
        self.nextButton.setIcon(self.icons.nextIcon())
        self.nextButton.setFlat(True)
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setToolTip("Next Page")
        self.nextButton.clicked.connect(self.nextPage)
        self.footerLayout.addWidget(self.nextButton)
        self.dialogLayout.addWidget(self.footerWidget)

        QtCore.QMetaObject.connectSlotsByName(dialog)
        return dialog

    def getPluginWidget(self, pluginData=PluginData):
        moVersion = self.organiser.appVersion().canonicalString()
        currentPlugin = pluginData.current(moVersion) # most recent working plugin.
        currentSupported = currentPlugin and not (currentPlugin.maxSupport() == "" or currentPlugin.minSupport() == "" or self.utilities.versionIsNewer(currentPlugin.maxSupport(), moVersion) or self.utilities.versionIsNewer(moVersion, currentPlugin.minSupport()))
        latestPlugin = pluginData.latest() # most recent overall plugin.
        installed = self.pluginfinder.installer.isInstalled(pluginData.identifier())
        installedVersion = self.pluginfinder.installer.installedVersion(pluginData.identifier())
        installedSpecific = pluginData.specificVersion(str(installedVersion))
        totalDownloads = self.pluginfinder.search.getInstallCount(pluginData.identifier())

        showUpdateIcon = False
        showUnsupportedUpdateIcon = False
        showUnsupportedInstallIcon = False
        showNotWorkingIcon = False
        showNotWorkingUpdateIcon = False
        canUpdate = False
        showVersion = False
        showNoDownloadIcon = False

        displayVersion = ""
        displayDate = ""
        changelog = []
        if latestPlugin:
            displayVersion = latestPlugin.version()
            displayDate = datetime.fromisoformat(latestPlugin.released()).strftime("%d %b %Y") + " "
            changelog = latestPlugin.releaseNotes()
        if currentPlugin and self.utilities.versionIsNewer(installedVersion, currentPlugin.version()):
            displayVersion = currentPlugin.version()
            displayDate = datetime.fromisoformat(currentPlugin.released()).strftime("%d %b %Y") + " "
            changelog = currentPlugin.releaseNotes()
            
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

        # Main Widget Container
        widget = QtWidgets.QWidget()
        widget.setObjectName("widget")
        widget.resize(949, 102)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        pluginLayout = QtWidgets.QVBoxLayout(widget)
        pluginLayout.setContentsMargins(0, 0, 0, 0)
        pluginLayout.setSpacing(0)
        pluginLayout.setObjectName("pluginLayout")
        
        # Plugin Header Container
        pluginHeaderWidget = QtWidgets.QWidget(widget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginHeaderWidget.sizePolicy().hasHeightForWidth())
        pluginHeaderWidget.setSizePolicy(sizePolicy)
        pluginHeaderWidget.setObjectName("pluginHeaderWidget")
        pluginHeaderLayout = QtWidgets.QHBoxLayout(pluginHeaderWidget)
        pluginHeaderLayout.setContentsMargins(0, 0, 0, 0)
        pluginHeaderLayout.setSpacing(5)
        pluginHeaderLayout.setObjectName("pluginHeaderLayout")
        
        # Plugin Label Container
        pluginLabelWidget = QtWidgets.QWidget(pluginHeaderWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginLabelWidget.sizePolicy().hasHeightForWidth())
        pluginLabelWidget.setSizePolicy(sizePolicy)
        pluginLabelWidget.setObjectName("pluginLabelWidget")
        pluginLabelLayout = QtWidgets.QVBoxLayout(pluginLabelWidget)
        pluginLabelLayout.setContentsMargins(0, 0, 0, 0)
        pluginLabelLayout.setSpacing(0)
        pluginLabelLayout.setObjectName("pluginLabelLayout")

        # Plugin Title Container
        pluginTitleWidget = QtWidgets.QWidget(pluginLabelWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginTitleWidget.sizePolicy().hasHeightForWidth())
        pluginTitleWidget.setSizePolicy(sizePolicy)
        pluginTitleWidget.setObjectName("pluginTitleWidget")
        pluginTitleLayout = QtWidgets.QHBoxLayout(pluginTitleWidget)
        pluginTitleLayout.setContentsMargins(0, 0, 0, 0)
        pluginTitleLayout.setSpacing(0)
        pluginTitleLayout.setObjectName("pluginTitleLayout")

        # Plugin Release Type Icon
        hasVersionIcon = False
        if displayVersion != "":
            ver = mobase.VersionInfo(displayVersion).canonicalString()
            isAlpha = self.pluginfinder.utilities.alphaVersion(ver)
            isBeta = self.pluginfinder.utilities.betaVersion(ver)
            isRC = self.pluginfinder.utilities.rcVersion(ver)
            if isAlpha or isBeta or isRC:
                releaseTypeIcon = QtWidgets.QLabel(pluginTitleWidget)
                sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(releaseTypeIcon.sizePolicy().hasHeightForWidth())
                releaseTypeIcon.setSizePolicy(sizePolicy)
                releaseTypeIcon.setMaximumSize(QtCore.QSize(16, 16777215))
                releaseTypeIcon.setText("")
                releaseTypeIcon.setObjectName("releaseTypeIcon")
                if isAlpha:
                    releaseTypeIcon.setPixmap(self.icons.alphaIcon().pixmap(QSize(16, 16)))
                    releaseTypeIcon.setToolTip("This plugin is currently in alpha.")
                    hasVersionIcon = True
                elif isBeta:
                    releaseTypeIcon.setPixmap(self.icons.betaIcon().pixmap(QSize(16, 16)))
                    releaseTypeIcon.setToolTip("This plugin is currently in beta.")
                    hasVersionIcon = True
                elif isRC:
                    releaseTypeIcon.setPixmap(self.icons.gammaIcon().pixmap(QSize(16, 16)))
                    releaseTypeIcon.setToolTip("This plugin is currently a release candidate.")
                    hasVersionIcon = True
                pluginTitleLayout.addWidget(releaseTypeIcon)

        # Plugin Title
        pluginNameLabel = QtWidgets.QLabel(pluginTitleWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginNameLabel.sizePolicy().hasHeightForWidth())
        pluginNameLabel.setSizePolicy(sizePolicy)
        pluginNameLabel.setScaledContents(False)
        pluginNameLabel.setObjectName("pluginNameLabel")
        pluginNameLabel.setText("<html><head/><body><p><span style=\"font-size:11pt;font-weight:600;\">" + pluginData.name() + "</span></p></body></html>")
        pluginTitleLayout.addWidget(pluginNameLabel)

        # Plugin Tag
        pluginTagIcon = QtWidgets.QLabel(pluginTitleWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginTagIcon.sizePolicy().hasHeightForWidth())
        pluginTagIcon.setSizePolicy(sizePolicy)
        pluginTagIcon.setMaximumSize(QtCore.QSize(16777215, 16777215))
        pluginTagIcon.setText("")
        pluginTagIcon.setObjectName("pluginTagIcon")
        pluginTitleLayout.addWidget(pluginTagIcon)
        # When tags are implemented, add an icon to this label.

        pluginLabelLayout.addWidget(pluginTitleWidget)

        # Subheading Container
        pluginSubheadingWidget = QtWidgets.QWidget(pluginLabelWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginSubheadingWidget.sizePolicy().hasHeightForWidth())
        pluginSubheadingWidget.setSizePolicy(sizePolicy)
        pluginSubheadingWidget.setObjectName("pluginSubheadingWidget")
        pluginSubheadingLayout = QtWidgets.QHBoxLayout(pluginSubheadingWidget)
        pluginSubheadingLayout.setContentsMargins(0, 0, 0, 0)
        pluginSubheadingLayout.setSpacing(0)
        pluginSubheadingLayout.setObjectName("pluginSubheadingLayout")

        # Release Date
        pluginReleaseDate = QtWidgets.QLabel(pluginSubheadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginReleaseDate.sizePolicy().hasHeightForWidth())
        pluginReleaseDate.setSizePolicy(sizePolicy)
        pluginReleaseDate.setObjectName("pluginReleaseDate")
        pluginReleaseDate.setText("<html><head/><body><p><span style=\" font-size:7pt;\">" + displayDate + "</span></p></body></html>")
        pluginReleaseDate.setToolTip("The date of the most recent release.")
        pluginSubheadingLayout.addWidget(pluginReleaseDate)

        # Author
        authorText = ""
        if pluginData.author() and pluginData.author() != "":
            authorText = "by " + pluginData.author()
        pluginAuthorLabel = QtWidgets.QLabel(pluginSubheadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginAuthorLabel.sizePolicy().hasHeightForWidth())
        pluginAuthorLabel.setSizePolicy(sizePolicy)
        pluginAuthorLabel.setObjectName("pluginAuthorLabel")
        pluginAuthorLabel.setText("<html><head/><body><p><span style=\" font-size:7pt; font-style:italic;\">" + authorText + "</span></p></body></html>")
        pluginAuthorLabel.setToolTip("The name of the plugin author.")
        pluginSubheadingLayout.addWidget(pluginAuthorLabel)

        # Download Count
        downloadsIcon = QtWidgets.QLabel(pluginSubheadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(downloadsIcon.sizePolicy().hasHeightForWidth())
        downloadsIcon.setSizePolicy(sizePolicy)
        downloadsIcon.setMaximumSize(QtCore.QSize(16, 16777215))
        downloadsIcon.setText("")
        downloadsIcon.setPixmap(self.icons.downloadIcon().pixmap(QSize(16,16)))
        downloadsIcon.setToolTip("Total installations through Plugin Finder. Uninstallations are subtracted.")
        downloadsIcon.setObjectName("downloadsIcon")
        pluginSubheadingLayout.addWidget(downloadsIcon)
        pluginInstallCount = QtWidgets.QLabel(pluginSubheadingWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginInstallCount.sizePolicy().hasHeightForWidth())
        pluginInstallCount.setSizePolicy(sizePolicy)
        pluginInstallCount.setObjectName("pluginInstallCount")
        pluginInstallCount.setToolTip("Total installations through Plugin Finder. Uninstallations are subtracted.")
        pluginInstallCount.setText("<html><head/><body><p><span style=\" font-size:7pt;\">" + str(totalDownloads) + "</span></p></body></html>")
        pluginSubheadingLayout.addWidget(pluginInstallCount)

        pluginLabelLayout.addWidget(pluginSubheadingWidget)
        pluginHeaderLayout.addWidget(pluginLabelWidget)

        # Update Info Widget
        pluginUpdateWidget = QtWidgets.QWidget(pluginHeaderWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginUpdateWidget.sizePolicy().hasHeightForWidth())
        pluginUpdateWidget.setSizePolicy(sizePolicy)
        pluginUpdateWidget.setObjectName("pluginUpdateWidget")
        pluginUpdateLayout = QtWidgets.QHBoxLayout(pluginUpdateWidget)
        pluginUpdateLayout.setContentsMargins(0, 0, 0, 0)
        pluginUpdateLayout.setObjectName("pluginUpdateLayout")

        # Plugin Update Icon
        updateIcon = QtWidgets.QLabel(pluginUpdateWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(updateIcon.sizePolicy().hasHeightForWidth())
        updateIcon.setSizePolicy(sizePolicy)
        updateIcon.setText("")
        updateIcon.setScaledContents(False)
        updateIcon.setAlignment(qtAlign.AlignCenter)
        updateIcon.setMinimumSize(16, 16)
        updateIcon.setObjectName("updateIcon")
        if showUpdateIcon:
            updateIcon.setPixmap(self.icons.updateIcon().pixmap(QSize(16, 16)))
            updateIcon.setToolTip("There is a new update available!")
        elif showUnsupportedUpdateIcon:
            updateIcon.setPixmap(self.icons.updateAltIcon().pixmap(QSize(16,16)))
            updateIcon.setToolTip("There is a new update available but this update has not been tested with this version of Mod Organizer and may not work correctly.")
        elif showNotWorkingIcon:
            updateIcon.setPixmap(self.icons.stopIcon().pixmap(QSize(16,16)))
            updateIcon.setToolTip("There is no version of this plugin that works with this version of Mod Organizer.")
        elif showNotWorkingUpdateIcon:
            updateIcon.setPixmap(self.icons.noUpdateIcon().pixmap(QSize(16,16)))
            updateIcon.setToolTip("There is a new update available but does not work with this version of Mod Organizer.")
        elif showUnsupportedInstallIcon:
            updateIcon.setPixmap(self.icons.warningIcon().pixmap(QSize(16,16)))
            updateIcon.setToolTip("This plugin has not been tested with this version of Mod Organizer and may not work correctly.")
        elif installed:
            updateIcon.setPixmap(self.icons.checkIcon().pixmap(QSize(16,16)))
            updateIcon.setToolTip("This plugin is up to date.")
        elif showNoDownloadIcon:
            updateIcon.setPixmap(self.icons.infoIcon().pixmap(QSize(16,16)))
            updateIcon.setToolTip("This plugin cannot be installed through Plugin Finder.")
        pluginUpdateLayout.addWidget(updateIcon)

        # Version Info Container
        pluginVersionWidget = QtWidgets.QWidget(pluginUpdateWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginVersionWidget.sizePolicy().hasHeightForWidth())
        pluginVersionWidget.setSizePolicy(sizePolicy)
        pluginVersionWidget.setMinimumWidth(70)
        pluginVersionWidget.setObjectName("pluginVersionWidget")
        pluginVersionLayout = QtWidgets.QVBoxLayout(pluginVersionWidget)
        pluginVersionLayout.setContentsMargins(0, 0, 0, 0)
        pluginVersionLayout.setSpacing(3)
        pluginVersionLayout.setObjectName("pluginVersionLayout")

        # Current Version
        currentVersionLabel = QtWidgets.QLabel(pluginVersionWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(currentVersionLabel.sizePolicy().hasHeightForWidth())
        currentVersionLabel.setSizePolicy(sizePolicy)
        currentVersionLabel.setObjectName("currentVersionLabel")
        if showVersion:
            string = "<p>Latest Version <i>" + displayDate + "</i></p><ul>"
            for note in changelog:
                string = string + "<li>" + str(note) + "</li>"
            string = string + "</ul>"
            currentVersionLabel.setToolTip(string)
            currentVersionLabel.setText("<html><head/><body><p><span style=\" font-size:7pt;\">v" + mobase.VersionInfo(displayVersion).canonicalString() + "</span></p></body></html>")
        pluginVersionLayout.addWidget(currentVersionLabel)

        # Installed Version
        installedVersionLabel = QtWidgets.QLabel(pluginVersionWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(installedVersionLabel.sizePolicy().hasHeightForWidth())
        installedVersionLabel.setSizePolicy(sizePolicy)
        installedVersionLabel.setObjectName("installedVersionLabel")
        if installed:
            string = "<p>Installed Version</p>"
            if installedSpecific:
                string = "<p>Installed Version <i>" + datetime.fromisoformat(installedSpecific.released()).strftime("%d %b %Y") + "</i></p>"
                string = string + "<ul>"
                for note in installedSpecific.releaseNotes():
                    string = string + "<li>" + str(note) + "</li>"
                string = string + "</ul>"
            installedVersionLabel.setToolTip(string)
            installedVersionLabel.setText("<html><head/><body><p><span style=\" font-size:7pt;\">v" + mobase.VersionInfo(installedVersion).canonicalString() + "</span></p></body></html>")
        pluginVersionLayout.addWidget(installedVersionLabel)

        pluginUpdateLayout.addWidget(pluginVersionWidget)
        pluginHeaderLayout.addWidget(pluginUpdateWidget)

        # Installation Buttons Container
        pluginInstallWidget = QtWidgets.QWidget(pluginHeaderWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginInstallWidget.sizePolicy().hasHeightForWidth())
        pluginInstallWidget.setSizePolicy(sizePolicy)
        pluginInstallWidget.setObjectName("pluginInstallWidget")
        pluginInstallLayout = QtWidgets.QHBoxLayout(pluginInstallWidget)
        pluginInstallLayout.setContentsMargins(0, 0, 0, 0)
        pluginInstallLayout.setSpacing(0)
        pluginInstallLayout.setObjectName("pluginInstallLayout")

        # Install Button
        installButton = QtWidgets.QPushButton(pluginInstallWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setRetainSizeWhenHidden(True)
        sizePolicy.setHeightForWidth(installButton.sizePolicy().hasHeightForWidth())
        installButton.setSizePolicy(sizePolicy)
        installButton.setText("")
        installButton.setFlat(True)
        installButton.setIcon(self.icons.installIcon())
        installButton.setObjectName("installButton")
        installButton.setToolTip("Install/Update")
        if canUpdate:
            installButton.clicked.connect(lambda: self.installClick(pluginData.identifier()))
        else:
            installButton.setVisible(False)
        pluginInstallLayout.addWidget(installButton)

        # Uninstall Button
        uninstallButton = QtWidgets.QPushButton(pluginInstallWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setRetainSizeWhenHidden(True)
        sizePolicy.setHeightForWidth(uninstallButton.sizePolicy().hasHeightForWidth())
        uninstallButton.setSizePolicy(sizePolicy)
        uninstallButton.setFlat(True)
        uninstallButton.setText("")
        uninstallButton.setIcon(self.icons.trashIcon())
        uninstallButton.setObjectName("uninstallButton")
        uninstallButton.setToolTip("Uninstall")
        if installed and pluginData.identifier() != "pluginfinder":
            uninstallButton.clicked.connect(lambda: self.uninstallClick(pluginData.identifier()))
        else:
            uninstallButton.setVisible(False)
        pluginInstallLayout.addWidget(uninstallButton)

        pluginHeaderLayout.addWidget(pluginInstallWidget)

        # Link Buttons Container
        pluginLinksWidget = QtWidgets.QWidget(pluginHeaderWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginLinksWidget.sizePolicy().hasHeightForWidth())
        pluginLinksWidget.setSizePolicy(sizePolicy)
        pluginLinksWidget.setObjectName("pluginLinksWidget")
        pluginLinksLayout = QtWidgets.QHBoxLayout(pluginLinksWidget)
        pluginLinksLayout.setContentsMargins(0, 0, 0, 0)
        pluginLinksLayout.setSpacing(0)
        pluginLinksLayout.setObjectName("pluginLinksLayout")

        # Docs Button
        docsButton = QtWidgets.QPushButton(pluginLinksWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(docsButton.sizePolicy().hasHeightForWidth())
        sizePolicy.setRetainSizeWhenHidden(True)
        docsButton.setSizePolicy(sizePolicy)
        docsButton.setFlat(True)
        docsButton.setText("")
        docsButton.setIcon(self.icons.docsIcon())
        docsButton.setObjectName("docsButton")
        docsButton.setToolTip("Documentation")
        if pluginData.docsUrl() != "":
            docsButton.clicked.connect(lambda: webbrowser.open(str(pluginData.docsUrl())))
        else:
            docsButton.setVisible(False)
        pluginLinksLayout.addWidget(docsButton)

        # Github Button
        githubButton = QtWidgets.QPushButton(pluginLinksWidget)
        githubButton.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(docsButton.sizePolicy().hasHeightForWidth())
        sizePolicy.setRetainSizeWhenHidden(True)
        githubButton.setSizePolicy(sizePolicy)
        githubButton.setText("")
        githubButton.setIcon(self.icons.githubIcon())
        githubButton.setObjectName("githubButton")
        githubButton.setToolTip("Github")
        if pluginData.githubUrl() != "":
            githubButton.clicked.connect(lambda: webbrowser.open(str(pluginData.githubUrl())))
        else:
            githubButton.setVisible(False)
        pluginLinksLayout.addWidget(githubButton)

        # Nexus Button
        nexusButton = QtWidgets.QPushButton(pluginLinksWidget)
        nexusButton.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(docsButton.sizePolicy().hasHeightForWidth())
        sizePolicy.setRetainSizeWhenHidden(True)
        nexusButton.setSizePolicy(sizePolicy)
        nexusButton.setText("")
        nexusButton.setIcon(self.icons.nexusIcon())
        nexusButton.setObjectName("nexusButton")
        nexusButton.setToolTip("Nexus")
        if pluginData.nexusUrl() != "":
            nexusButton.clicked.connect(lambda: webbrowser.open(str(pluginData.nexusUrl())))
        else:
            nexusButton.setVisible(False)
        pluginLinksLayout.addWidget(nexusButton)

        pluginHeaderLayout.addWidget(pluginLinksWidget)
        pluginLayout.addWidget(pluginHeaderWidget)

        # Description
        pluginDescription = QtWidgets.QLabel(widget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginDescription.sizePolicy().hasHeightForWidth())
        pluginDescription.setSizePolicy(sizePolicy)
        pluginDescription.setScaledContents(False)
        pluginDescription.setAlignment(qtAlign.AlignLeading|qtAlign.AlignLeft|qtAlign.AlignTop)
        pluginDescription.setWordWrap(True)
        pluginDescription.setObjectName("pluginDescription")
        if pluginData.description() and pluginData.description() != "":
            pluginDescription.setToolTip(pluginData.description())
            pluginDescription.setText(pluginData.description())
        pluginLayout.addWidget(pluginDescription)
        
        QtCore.QMetaObject.connectSlotsByName(widget)
        return widget

    def getEmptyPluginWidget(self):
        # Main Widget Container
        widget = QtWidgets.QWidget()
        widget.setObjectName("widget")
        widget.resize(949, 102)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)
        pluginLayout = QtWidgets.QVBoxLayout(widget)
        pluginLayout.setContentsMargins(0, 0, 0, 0)
        pluginLayout.setSpacing(0)
        pluginLayout.setObjectName("pluginLayout")

        # Plugin Title
        pluginNameLabel = QtWidgets.QLabel(widget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginNameLabel.sizePolicy().hasHeightForWidth())
        pluginNameLabel.setSizePolicy(sizePolicy)
        pluginNameLabel.setScaledContents(False)
        pluginNameLabel.setObjectName("pluginNameLabel")
        pluginNameLabel.setText("<html><head/><body><p><span style=\"font-size:11pt;font-weight:600;\">&nbsp;</span></p></body></html>")
        pluginLayout.addWidget(pluginNameLabel)

        # Release Date
        pluginReleaseDate = QtWidgets.QLabel(widget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Maximum, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginReleaseDate.sizePolicy().hasHeightForWidth())
        pluginReleaseDate.setSizePolicy(sizePolicy)
        pluginReleaseDate.setObjectName("pluginReleaseDate")
        pluginReleaseDate.setText("<html><head/><body><p><span style=\" font-size:7pt;\">&nbsp;</span></p></body></html>")
        pluginLayout.addWidget(pluginReleaseDate)

        # Description
        pluginDescription = QtWidgets.QLabel(widget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginDescription.sizePolicy().hasHeightForWidth())
        pluginDescription.setSizePolicy(sizePolicy)
        pluginDescription.setScaledContents(False)
        pluginDescription.setAlignment(qtAlign.AlignLeading|qtAlign.AlignLeft|qtAlign.AlignTop)
        pluginDescription.setWordWrap(True)
        pluginDescription.setObjectName("pluginDescription")
        pluginLayout.addWidget(pluginDescription)
        
        QtCore.QMetaObject.connectSlotsByName(widget)
        return widget

    def getPluginSeparator(self):
        pluginSeparator = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pluginSeparator.sizePolicy().hasHeightForWidth())
        pluginSeparator.setSizePolicy(sizePolicy)
        pluginSeparator.setFrameShape(qtHLine)
        pluginSeparator.setFrameShadow(qtSunken)
        pluginSeparator.setObjectName("pluginSeparator")
        return pluginSeparator
        