import mobase, os
from pathlib import Path
from ..core.openmwplayer_settings import OpenMWPlayerSettings
from .openmwplayer_strings import OpenMWPlayerStrings
from ....common.common_qt import *
from ....common.common_utilities import *

class OpenMWPlayerDeploy():
    """ OpenMW Player deploy module, handles deploying openmw.cfg and settings.cfg when running OpenMW."""

    def __init__(self, organiser:mobase.IOrganizer, settings:OpenMWPlayerSettings, strings:OpenMWPlayerStrings):
        self._organiser = organiser
        self._settings = settings
        self._strings = strings

    def deployCfg(self):
        openmwCfg = self._strings.openmwCfgPath()
        openmwBackupCfg = f"{openmwCfg}.omwpbackup"
        customOpenmwCfg = self._strings.customOpenmwCfgPath()

        settingsCfg = self._strings.settingsCfgPath()
        settingsBackupCfg = f"{settingsCfg}.omwpbackup"
        customSettingsCfg = self._strings.customSettingsCfgPath()

        if openmwCfg is not None and Path(openmwCfg).exists() and not Path(openmwBackupCfg).exists():
            moveFile(openmwCfg, openmwBackupCfg)
        if settingsCfg is not None and Path(settingsCfg).exists() and not Path(settingsBackupCfg).exists():
            moveFile(settingsCfg, settingsBackupCfg)

        if customOpenmwCfg is not None and Path(customOpenmwCfg).exists():
            copyFile(customOpenmwCfg, openmwCfg)
        if customSettingsCfg is not None and Path(customSettingsCfg).exists():
            copyFile(customSettingsCfg, settingsCfg)

    def restoreCfg(self):
        openmwCfg = self._strings.openmwCfgPath()
        openmwBackupCfg = f"{openmwCfg}.omwpbackup"
        customOpenmwCfg = self._strings.customOpenmwCfgPath()
        if openmwCfg is not None and Path(openmwCfg).exists() and Path(openmwBackupCfg).exists():
            copyFile(openmwCfg, customOpenmwCfg)
            moveFile(openmwBackupCfg, openmwCfg)

        settingsCfg = self._strings.settingsCfgPath()
        settingsBackupCfg = f"{settingsCfg}.omwpbackup"
        customSettingsCfg = self._strings.customSettingsCfgPath()
        if settingsCfg is not None and Path(settingsCfg).exists() and Path(settingsBackupCfg).exists():
            copyFile(settingsCfg, customSettingsCfg)
            moveFile(settingsBackupCfg, settingsCfg)

