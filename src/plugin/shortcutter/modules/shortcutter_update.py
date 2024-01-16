import mobase
from .shortcutter_strings import ShortcutterStrings
from ....common.common_utilities import downloadFile, loadJson
from ....common.common_log import CommonLog

class ShortcutterUpdate:
    """Shortcutter update module, used to check if Root Builder is on the current version."""

    def __init__(self, organiser: mobase.IOrganizer, plugin: mobase.IPlugin, strings: ShortcutterStrings, log: CommonLog) -> None:
        self._organiser = organiser
        self._plugin = plugin
        self._strings = strings
        self._log = log

    _scManifest = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/shortcutter.json"
    _scVersionsKey = "Versions"
    _scVersionKey = "Version"

    def getLatestVersion(self) -> mobase.VersionInfo:
        """Checks if Root Builder needs an update."""
        updatePath = self._strings.updateFilePath
        if downloadFile(self._scManifest, updatePath):
            rbData = loadJson(updatePath)
            rbVersions = rbData[self._scVersionsKey]
            thisVersionInfo = self._plugin.version()
            newestVersionInfo = None
            for version in rbVersions:
                testVersion = version[self._scVersionKey]
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
