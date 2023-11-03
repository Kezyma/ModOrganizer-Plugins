import mobase
from .rootbuilder_strings import RootBuilderStrings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog

class RootBuilderUpdate():
    """Root Builder update module, used to check if Root Builder is on the current version."""

    def __init__(self, organiser:mobase.IOrganizer, plugin:mobase.IPlugin, strings:RootBuilderStrings,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._plugin = plugin
        self._strings = strings
        self._util = utilities
        self._log = log

    _rbManifest = "https://raw.githubusercontent.com/Kezyma/ModOrganizer-Plugins/main/directory/plugins/rootbuilder.json"
    _rbVersionsKey = "Versions"
    _rbVersionKey = "Version"

    def getLatestVersion(self) -> mobase.VersionInfo:
        """Checks if Root Builder needs an update."""
        updatePath = self._strings.rbUpdateFilePath()
        if self._util.downloadFile(self._rbManifest, updatePath):
            rbData = self._util.loadJson(updatePath)
            rbVersions = rbData[self._rbVersionsKey]
            thisVersionInfo = self._plugin.version()
            newestVersionInfo = None
            for version in rbVersions:
                testVersion = version[self._rbVersionKey]
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
