import mobase, threading
from ..core.pluginfinder_plugin import PluginFinderPlugin
from ..modules.pluginfinder_menu import PluginFinderMenu
from ....base.base_dialog import BaseDialog
from ....common.common_qt import *
from ....common.common_icons import *
from ..models.pluginfinder_installdata import *
from ..models.pluginfinder_manifestdata import *
from ..models.pluginfinder_versiondata import *

class PluginFinderUpdater(PluginFinderPlugin, mobase.IPluginDiagnose):
    def __init__(self):
        super().__init__()

    def init(self, organiser:mobase.IOrganizer):
        res = super().init(organiser)
        self.notifications()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def icon(self):
        return LINK_ALT_ICON

    def name(self):
        return f"{self.baseName()} Updater"

    def displayName(self):
        return f"{self.baseDisplayName()} Updater"

    def description(self):
        return self.__tr("Notifies the user of plugin updates.")
    
    def settings(self):
        return []
    
    def master(self):
        return self.baseName()
    
    def activeProblems(self) -> List[int]:
        return list(self._notifications.keys())
    
    def fullDescription(self, key: int) -> str:
        return self._description[key]
    
    def shortDescription(self, key: int) -> str:
        return self._shortDesc[key]
    
    def hasGuidedFix(self, key: int) -> bool:
        return True
    
    def startGuidedFix(self, key: int) -> None:
        self._pluginFinder._install.installPlugin(self._notifications[key])
        self._pluginFinder._install.reloadData()

    _notifications = {}
    _shortDesc = {}
    _description = {}
    def notifications(self):
        installData = self._pluginFinder._install.loadInstallData()
        needUpdate = self._pluginFinder._search.searchDirectory(working=True, update=True)
        ix = 0
        for key in needUpdate:
            manifest = self._pluginFinder._directory.getPluginManifest(key)
            data = installData[key]
            currentVer = mobase.VersionInfo(data[VERSION])
            latestVerData = self._pluginFinder._directory.getLatestVersionData(key)
            latestVer = mobase.VersionInfo(latestVerData[VERSION])
            shortDesc = f"An update is available for {manifest[NAME]}."
            longDesc = f"<b>Plugin: {manifest[NAME]}</b><br/><b>Current: {currentVer.displayString()}</b><br/><b>Latest: {latestVer.displayString()}</b><br/>"
            if RELEASENOTES in manifest:
                longDesc = f"{longDesc}<b>Release Notes</b><br/><ul>"
                for note in manifest[RELEASENOTES]:
                    longDesc = f"{longDesc}<li>{note}</li>"
                longDesc = f"{longDesc}</ul>"
            self._notifications[ix] = key
            self._shortDesc[ix] = shortDesc
            self._description[ix] = longDesc
            ix += 1

    
