import mobase
from .profilesync_strings import ProfileSyncStrings
from ....common.common_utilities import downloadFile, loadJson
from ....common.common_log import CommonLog

class ProfileSyncUpdate:
    """Profile Sync update module, used to check if Profile Sync is on the current version."""

    def __init__(self, organiser: mobase.IOrganizer, plugin: mobase.IPlugin, strings: ProfileSyncStrings, log: CommonLog) -> None:
        self._organiser = organiser
        self._plugin = plugin
        self._strings = strings
        self._log = log

    _rbManifest = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/profilesync.json"
    _rbVersionsKey = "Versions"
    _rbVersionKey = "Version"

    def getLatestVersion(self) -> mobase.VersionInfo:
        """Checks if Profile Sync needs an update."""
        updatePath = self._strings.psUpdateFilePath
        if downloadFile(self._rbManifest, updatePath):
            rbData = loadJson(updatePath)
            rbVersions = rbData[self._rbVersionsKey]
            thisVersionInfo = self._plugin.version()
            newestVersionInfo = None
            for version in rbVersions:
                testVersion = version[self._rbVersionKey]
                testVersionInfo = mobase.VersionInfo(testVersion)
                if testVersionInfo > thisVersionInfo:
                    if newestVersionInfo == None or testVersionInfo > newestVersionInfo:
                        newestVersionInfo = testVersionInfo
            if newestVersionInfo != None:
                return newestVersionInfo
            else:
                return None
        else:
            self._log.warning("Could not retrieve update data.")
            return None
