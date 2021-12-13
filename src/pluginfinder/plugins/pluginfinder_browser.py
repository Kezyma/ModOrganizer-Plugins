from PyQt5.QtWidgets import QFileDialog, QFileIconProvider, QFormLayout, QInputDialog, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QCoreApplication, qInfo, QSize
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileIconProvider
from ..pluginfinder_plugin import PluginFinderPlugin
from ..models.plugin_data import PluginData
from ...shared.shared_utilities import SharedUtilities
import mobase, webbrowser

class PluginFinderBrowser(PluginFinderPlugin, mobase.IPluginTool):
    
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.page = 1
        self.pageSize = 7
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
        dialog.resize(620, 675)
        dialog.setMinimumSize(QtCore.QSize(620, 675))
        dialog.setMaximumSize(QtCore.QSize(620, 675))
        dialog.setWindowIcon(self.icons.pluginIcon())

        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setObjectName("verticalLayout")

        self.searchWidget = QtWidgets.QWidget(dialog)
        self.searchWidget.setMinimumSize(QtCore.QSize(0, 26))
        self.searchWidget.setMaximumSize(QtCore.QSize(16777215, 26))
        self.searchWidget.setObjectName("searchWidget")
        self.searchText = QtWidgets.QLineEdit(self.searchWidget)
        self.searchText.setGeometry(QtCore.QRect(0, 0, 526, 21))
        self.searchText.setObjectName("searchText")
        self.searchText.setPlaceholderText("Search")
        self.installedCheck = QtWidgets.QCheckBox(self.searchWidget)
        self.installedCheck.setGeometry(QtCore.QRect(535, 0, 66, 21))
        self.installedCheck.setObjectName("installedCheck")
        self.installedCheck.setText("Installed")
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
        pluginDesc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        pluginDesc.setWordWrap(True)
        pluginDesc.setObjectName("pluginDesc")        
        pluginDesc.setText(pluginData.description())

        plugin = pluginData.current(self.organiser.appVersion().canonicalString())
        installed = False
        installedVersion = ""
        currentVersion = plugin.version()
        updateAvailabe = self.utilities.versionIsNewer(installedVersion, currentVersion)

        if installed:
            pluginVersion = QtWidgets.QLabel(widget)
            pluginVersion.setGeometry(QtCore.QRect(345, 15, 41, 11))
            pluginVersion.setObjectName("pluginVersion")
            pluginVersion.setToolTip("Installed Version")
            pluginVersion.setText("<html><head/><body><p><span style=\" font-size:7pt;\">v" + installedVersion + "</span></p></body></html>")

        if !installed or updateAvailabe:
            pluginUpdateLabel = QtWidgets.QLabel(widget)
            pluginUpdateLabel.setGeometry(QtCore.QRect(345, 0, 41, 16))
            pluginUpdateLabel.setObjectName("pluginUpdateLabel")
            pluginUpdateLabel.setToolTip("New Version")
            pluginUpdateLabel.setText("<html><head/><body><p><span style=\" font-size:7pt;\">v" + currentVersion + "</span></p></body></html>")

        if updateAvailabe:
            updateIcon = QtWidgets.QLabel(widget)
            updateIcon.setGeometry(QtCore.QRect(325, 5, 16, 21))
            updateIcon.setText("")
            updateIcon.setPixmap(self.icons.syncIcon().pixmap(QSize(23, 23)))
            updateIcon.setObjectName("updateIcon")
            updateIcon.setToolTip("New Version Available")
            
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

        installButton = QtWidgets.QPushButton(widget)
        installButton.setGeometry(QtCore.QRect(390, 0, 40, 26))
        installButton.setText("")
        installButton.setIcon(self.icons.installIcon())
        installButton.setObjectName("installButton")
        installButton.setToolTip("Install/Update")

        line = QtWidgets.QFrame(widget)
        line.setGeometry(QtCore.QRect(0, 70, 601, 16))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")

        return widget
