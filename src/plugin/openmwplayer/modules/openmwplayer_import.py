import mobase, os
from pathlib import Path
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from .openmwplayer_strings import OpenMWPlayerStrings
from ....common.common_qt import *
from ....common.common_utilities import *

class OpenMWPlayerImport():
    """ OpenMW Player import module, handles importing openmw.cfg and settings.cfg. """

    def __init__(self, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings, strings:OpenMWPlayerStrings):
        self._organiser = organiser
        self._settings = settings
        self._strings = strings

    def importOpenmwCfg(self):
        # Get or request the openmw.cfg path.
        profile = self._organiser.profile().name()
        cfgPath = self._strings.openmwCfgPath()
        if cfgPath == None:
            manualPath = Path(QFileDialog.getOpenFileName(None, "Locate OpenMW Config File", ".", "OpenMW Config File (openmw.cfg)")[0])
            self._settings.updateSetting("openmwcfgpath", str(manualPath))
            cfgPath = self._strings.openmwCfgPath()
        # If the config actually exists, import it.
        if Path(cfgPath).exists():
            currentPath = self._strings.customOpenmwCfgPath(profile)
            # Delete any existing openmw.cfg
            if Path(currentPath).exists():
                deleteFile(currentPath)
            # Copy in the new one
            copyFile(cfgPath, currentPath)

    def importSettingsCfg(self):
        # Get or request the settings.cfg path.
        profile = self._organiser.profile().name()
        cfgPath = self._strings.settingsCfgPath()
        if cfgPath == None:
            cfgPath = self._strings.defaultSettingsCfgPath
        # If the config actually exists, import it.
        if Path(cfgPath).exists():
            currentPath = self._strings.customSettingsCfgPath(profile)
            # Delete any existing openmw.cfg
            if Path(currentPath).exists():
                deleteFile(currentPath)
            # Copy in the new one
            copyFile(cfgPath, currentPath)

    def exportOpenmwCfg(self):
        # Get or request the openmw.cfg path.
        profile = self._organiser.profile().name()
        cfgPath = self._strings.openmwCfgPath()
        if cfgPath == None:
            manualPath = Path(QFileDialog.getOpenFileName(None, "Locate OpenMW Config File", ".", "OpenMW Config File (openmw.cfg)")[0])
            self._settings.updateSetting("openmwcfgpath", str(manualPath))
            cfgPath = self._strings.openmwCfgPath()

        currentPath = self._strings.customOpenmwCfgPath(profile)
        # Export the current settings to that path.
        if Path(currentPath).exists():
            copyFile(currentPath, cfgPath)

    def exportSettingsCfg(self):
        # Get or request the settings.cfg path.
        profile = self._organiser.profile().name()
        cfgPath = self._strings.settingsCfgPath()
        if cfgPath != None:
            currentPath = self._strings.customSettingsCfgPath(profile)
            # Export the current settings to that path.
            if Path(currentPath).exists():
                copyFile(currentPath, cfgPath)


