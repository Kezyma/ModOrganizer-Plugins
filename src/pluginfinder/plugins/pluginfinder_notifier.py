import itertools
import os
import subprocess
from typing import Dict, List, NamedTuple, Optional

import mobase

from ..models.plugin_version import PluginVersion
from ..pluginfinder import PluginFinder
from ..pluginfinder_plugin import PluginFinderPlugin

try:
    from PyQt5.QtCore import qInfo
except ImportError:
    from PyQt6.QtCore import qInfo


class PluginUpdateNotification(NamedTuple):
    pluginId: str
    pluginName: str
    currentVersion: str
    newVersion: str
    releaseNotes: List[str]


class PluginFinderNotifier(PluginFinderPlugin, mobase.IPluginDiagnose):

    __notifications: Dict[int, PluginUpdateNotification] = {}

    def init(self, organiser: mobase.IOrganizer) -> bool:
        super().init(organiser)
        self.__pluginfinder = PluginFinder(self.organiser)
        self.__updateNotifications()
        return True

    def name(self) -> str:
        return "Plugin Finder Notifier"

    def author(self) -> str:
        return "Jonathan Feenstra"

    def description(self) -> str:
        return "Notifies the user when new updates are available for installed plugins."

    def settings(self) -> List[mobase.PluginSetting]:
        return []

    def activeProblems(self) -> List[int]:
        return list(self.__notifications.keys())

    def fullDescription(self, key: int) -> str:
        notification = self.__notifications[key]
        description = (
            f"{self.tr('A new update is available for plugin')} <b>{notification.pluginName}</b><br/><br/>"
            f"{self.tr('Current version')}: <b>{notification.currentVersion}</b><br/>"
            f"{self.tr('New version')}: <b>{notification.newVersion}</b>"
        )
        if notification.releaseNotes:
            description += (
                f"<br/><br/>{self.tr('Release notes')}:<ul>"
                + "".join(f"<li>{note}</li>" for note in notification.releaseNotes)
                + "</ul>"
            )
        return description

    def shortDescription(self, key: int) -> str:
        notification = self.__notifications[key]
        return self.tr("New update available for plugin {0}").format(
            notification.pluginName
        )

    def hasGuidedFix(self, key: int) -> bool:
        return True

    def startGuidedFix(self, key: int) -> None:
        self.__pluginfinder.install(self.__notifications[key].pluginId)
        self.__restartModOrganizer()

    def __updateNotifications(self) -> None:
        key = 0
        for (
            pluginId,
            currentData,
        ) in self.__pluginfinder.installer.getInstalledFiles().items():
            currentVersion = currentData["Version"]
            currentVersionInfo = mobase.VersionInfo(currentVersion)
            latestData = self.__pluginfinder.search.pluginData(pluginId)
            newVersionData = latestData.current(
                self.organiser.appVersion().canonicalString()
            )
            if newVersionData is not None:
                newVersion = newVersionData.version()
                newVersionInfo = mobase.VersionInfo(newVersion)
                if newVersionInfo > currentVersionInfo:
                    releaseNotes = self.__getReleaseNotesBetweenVersions(
                        latestData.versions(),
                        currentVersionInfo,
                        newVersionInfo,
                    )
                    self.__notifications[key] = PluginUpdateNotification(
                        pluginId,
                        latestData.name(),
                        currentVersion,
                        newVersion,
                        releaseNotes,
                    )
                    key += 1

    def __getReleaseNotesBetweenVersions(
        self,
        allVersions: Optional[List[PluginVersion]],
        currentVersionInfo: mobase.VersionInfo,
        newVersionInfo: mobase.VersionInfo,
    ) -> List[str]:
        return (
            list(
                itertools.chain.from_iterable(
                    version.releaseNotes()
                    for version in allVersions
                    if (versionInfo := mobase.VersionInfo(version.version()))
                    > currentVersionInfo
                    and versionInfo <= newVersionInfo
                )
            )
            if allVersions is not None
            else []
        )

    def __restartModOrganizer(self) -> None:
        qInfo("Plugin updated, restarting Mod Organizer.")
        tkExe = "C:/Windows/system32/taskkill.exe"
        moExe = self.__pluginfinder.paths.modOrganizerExePath()
        moKill = f'"{tkExe}" /F /IM ModOrganizer.exe && explorer "{moExe}"'
        qInfo(f"Executing command {moKill}")
        subprocess.call(moKill, shell=True, stdout=open(os.devnull, "wb"))
