import os
import subprocess
from typing import Dict, List, NamedTuple

import mobase

from ..pluginfinder import PluginFinder

try:
    from PyQt5.QtCore import QCoreApplication, qCritical, qInfo
    from PyQt5.QtWidgets import QMainWindow
except ImportError:
    from PyQt6.QtCore import QCoreApplication, qCritical, qInfo
    from PyQt6.QtWidgets import QMainWindow


class PluginUpdateNotification(NamedTuple):
    pluginId: str
    pluginName: str
    currentVersion: str
    latestVersion: str


class PluginFinderNotifier(mobase.IPluginDiagnose):

    __notifications: Dict[int, PluginUpdateNotification] = {}

    def init(self, organiser: mobase.IOrganizer) -> bool:
        self.__organiser = organiser
        if not self.__organiser.onUserInterfaceInitialized(
            self.__onUserInterfaceInitialized
        ):
            qCritical(
                self.__tr("Failed to register onUserInterfaceInitialized callback.")
            )
            return False
        self.__pluginfinder = PluginFinder(organiser)
        return True

    def name(self) -> str:
        return "Plugin Finder Notifier"

    def author(self) -> str:
        return "Jonathan Feenstra"

    def description(self) -> str:
        return "Notifies the user when new updates are available for installed plugins."

    def version(self) -> mobase.VersionInfo:
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.ALPHA)

    def settings(self) -> List[mobase.PluginSetting]:
        return []

    def activeProblems(self) -> List[int]:
        return list(self.__notifications.keys())

    def fullDescription(self, key: int) -> str:
        notification = self.__notifications[key]
        return self.__tr(
            "A new update is available for plugin <b>{0}</b><br/><br/>Current version: <b>{1}</b><br/>Latest supported version: <b>{2}</b>"
        ).format(
            notification.pluginName,
            notification.currentVersion,
            notification.latestVersion,
        )

    def shortDescription(self, key: int) -> str:
        notification = self.__notifications[key]
        return self.__tr("New update available for plugin {0}").format(
            notification.pluginName
        )

    def hasGuidedFix(self, key: int) -> bool:
        return True

    def startGuidedFix(self, key: int) -> None:
        self.__pluginfinder.install(self.__notifications[key].pluginId)
        self.__restartModOrganizer()

    def __onUserInterfaceInitialized(self, mainWindow: QMainWindow) -> None:
        key = 0
        for (
            pluginId,
            currentData,
        ) in self.__pluginfinder.installer.getInstalledFiles().items():
            currentVersion = currentData["Version"]
            latestData = self.__pluginfinder.search.pluginData(pluginId)
            latestSupportedVersion = latestData.current(
                self.__organiser.appVersion().canonicalString()
            ).version()
            if mobase.VersionInfo(latestSupportedVersion) > mobase.VersionInfo(
                currentVersion
            ):
                self.__notifications[key] = PluginUpdateNotification(
                    pluginId, latestData.name(), currentVersion, latestSupportedVersion
                )
                key += 1

    def __restartModOrganizer(self) -> None:
        qInfo("Plugin updated, restarting Mod Organizer.")
        tkExe = "C:/Windows/system32/taskkill.exe"
        moExe = self.__pluginfinder.paths.modOrganizerExePath()
        moKill = f'"{tkExe}" /F /IM ModOrganizer.exe && explorer "{moExe}"'
        qInfo(f"Executing command {moKill}")
        subprocess.call(moKill, shell=True, stdout=open(os.devnull, "wb"))

    def __tr(self, text: str) -> str:
        return QCoreApplication.translate(self.name(), text)
