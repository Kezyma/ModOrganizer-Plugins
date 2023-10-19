import mobase
from ...shared.shared_paths import SharedPaths
from .openmwplayer_settings import OpenMWPlayerSettings
from pathlib import Path
try:
    from PyQt5.QtCore import QCoreApplication, QStandardPaths
    from PyQt5.QtWidgets import QFileDialog
except:
    from PyQt6.QtCore import QCoreApplication, QStandardPaths
    from PyQt6.QtWidgets import QFileDialog
import os

class OpenMWPlayerPaths(SharedPaths):
    """ OpenMW Player path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer,settings=OpenMWPlayerSettings):
        self.settings = settings
        super().__init__("OpenMWPlayer", organiser) 

    def openMWCfgPath(self):
        """ Gets the path to the openmw.cfg file. """
        # Grab the saved setting if there is one.
        settingPath = Path(self.settings.cfgpath())
        if settingPath.is_file():
            return settingPath

        # Grab the default path if it exists.
        defaultLocation = Path(QStandardPaths.locate(QStandardPaths.DocumentsLocation, str(Path("My Games", "OpenMW", "openmw.cfg"))))
        if defaultLocation.is_file():
            self.organiser.setPluginSetting("OpenMWPlayer", "openmwcfgpath", str(defaultLocation))
            return defaultLocation

        # Otherwise, get the user to provide a path.
        manualPath = Path(QFileDialog.getOpenFileName(None, "Locate OpenMW Config File", ".", "OpenMW Config File (openmw.cfg)")[0])
        self.organiser.setPluginSetting("OpenMWPlayer", "openmwcfgpath", str(manualPath))
        return manualPath

    def openMwCustomSettingsPath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        profPath = Path(self.modOrganizerProfilesPath()) / profile
        return profPath

    def openMwSettingsCfgPath(self):
        # Grab the saved setting if there is one.
        settingPath = Path(self.openMWCfgPath())
        if settingPath.is_file():
            return settingPath.parent / "settings.cfg"

    def openMWSavedSettingsCfgPath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        return self.openMwCustomSettingsPath(profile) / "OpenMWSettingsCfg.txt"

    def openMwTempFilePath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        return self.openMwCustomSettingsPath(profile) / "openmw.cfg"

    def openMwGrassSettingsPath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        settingsPath = self.openMwCustomSettingsPath(profile) / "OpenMWGroundcover.txt"
        return Path(settingsPath)

    def openMwBsaSettingsPath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        settingsPath = self.openMwCustomSettingsPath(profile) / "OpenMWBsaRegister.txt"
        return Path(settingsPath)

    def openMwBaseCfgPath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        settingsPath = self.openMwCustomSettingsPath(profile) / "OpenMWConfig.txt"
        return Path(settingsPath)

    def openMwBaseSettingsPath(self, profile):
        """ Gets the path to the RootBuilder data folder for the current game. """
        settingsPath = self.openMwCustomSettingsPath(profile) / "OpenMWSettings.txt"
        return Path(settingsPath)

    def dummyEspPath(self):
        """ Gets the path to the base dummy esp. """
        espPath = Path(self.modOrganizerPluginPath()) / "openmwplayer" / "openmwplayer" / "openmwplayer.esp"
        return espPath