import mobase, webbrowser
from ..common.common_strings import CommonStrings
from ..common.common_utilities import downloadFile, loadJson
from ..common.common_icons import * 
from ..common.common_log import CommonLog
try:
    from .ui.qt6.update_widget import Ui_updateTabWidget
except:
    from .ui.qt5.update_widget import Ui_updateTabWidget

class BaseUpdate:
    """Plugin update module, used to check if the plugin is on the current version."""

    def __init__(self, manifestUrl:str, downloadUrl:str, plugin: mobase.IPlugin, strings: CommonStrings, log: CommonLog) -> None:
        self._manifest = manifestUrl
        self._download = downloadUrl
        self._plugin = plugin
        self._strings = strings
        self._log = log

    _versionsKey = "Versions"
    _versionKey = "Version"

    def getLatestVersion(self) -> mobase.VersionInfo:
        """Checks if this plugin needs an update."""
        updatePath = self._strings.updateFilePath
        if downloadFile(self._manifest, updatePath):
            rbData = loadJson(updatePath)
            rbVersions = rbData[self._versionsKey]
            thisVersionInfo = self._plugin.version()
            newestVersionInfo = None
            for version in rbVersions:
                testVersion = version[self._versionKey]
                testVersionInfo = mobase.VersionInfo(testVersion)
                if testVersionInfo > thisVersionInfo:
                    if newestVersionInfo is None or testVersionInfo > newestVersionInfo:
                        newestVersionInfo = testVersionInfo
            if newestVersionInfo is not None:
                return newestVersionInfo
            else:
                return None
        else:
            self._log.warning("Could not retrieve update data.")
            return None
        
    def configure(self, widget:Ui_updateTabWidget):
        self._widget = widget
        self._widget.updateFoundWidget.setVisible(False)
        self._widget.noUpdateWidget.setVisible(False)
        self._widget.checkUpdateButton.setIcon(REFRESH_ICON)
        self._widget.updateFoundButton.setIcon(DOWNLOAD_ICON)
        self._widget.checkUpdateLabel.setText(f"Check for a new version of {self._plugin.localizedName()}.")
        self._widget.noUpdateLabel.setText(f"{self._plugin.localizedName()} is up to date.")
        self._widget.updateFoundLabel.setText(f"New version of {self._plugin.localizedName()} is available.")
        self._widget.checkUpdateButton.clicked.connect(self.checkUpdate_clicked)

    def checkUpdate_clicked(self):
        """Checks for an update"""
        newVersion = self.getLatestVersion()
        hasUpdate = newVersion is not None
        self._widget.updateFoundWidget.setVisible(hasUpdate)
        self._widget.noUpdateWidget.setVisible(not hasUpdate)

    def updateFound_clicked(self):
        webbrowser.open(self._download)
