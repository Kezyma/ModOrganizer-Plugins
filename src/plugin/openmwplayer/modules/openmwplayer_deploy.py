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
        """Deploys custom configs to external locations for non-OpenMW.exe launches."""
        openmwCfg = self._strings.openmwCfgPath()
        customOpenmwCfg = self._strings.customOpenmwCfgPath()

        # Ensure target directory exists (handles fresh OpenMW installs)
        targetDir = Path(openmwCfg).parent
        if not targetDir.exists():
            os.makedirs(targetDir, exist_ok=True)

        openmwBackupCfg = f"{openmwCfg}.omwpbackup"
        # Only backup if original exists and backup doesn't
        if Path(openmwCfg).exists() and not Path(openmwBackupCfg).exists():
            moveFile(openmwCfg, openmwBackupCfg)
        # Deploy custom config if it exists
        if Path(customOpenmwCfg).exists():
            copyFile(customOpenmwCfg, openmwCfg)

        # Same for settings.cfg
        settingsCfg = self._strings.settingsCfgPath()
        customSettingsCfg = self._strings.customSettingsCfgPath()

        settingsBackupCfg = f"{settingsCfg}.omwpbackup"
        if Path(settingsCfg).exists() and not Path(settingsBackupCfg).exists():
            moveFile(settingsCfg, settingsBackupCfg)
        if Path(customSettingsCfg).exists():
            copyFile(customSettingsCfg, settingsCfg)

        # Same for launcher.cfg
        launcherCfg = self._strings.launcherCfgPath()
        customLauncherCfg = self._strings.customLauncherCfgPath()

        launcherBackupCfg = f"{launcherCfg}.omwpbackup"
        if Path(launcherCfg).exists() and not Path(launcherBackupCfg).exists():
            moveFile(launcherCfg, launcherBackupCfg)
        if Path(customLauncherCfg).exists():
            copyFile(customLauncherCfg, launcherCfg)

    def restoreCfg(self):
        """Restores original configs after non-OpenMW.exe launches."""
        openmwCfg = self._strings.openmwCfgPath()
        openmwBackupCfg = f"{openmwCfg}.omwpbackup"
        customOpenmwCfg = self._strings.customOpenmwCfgPath()

        if Path(openmwCfg).exists() and Path(openmwBackupCfg).exists():
            copyFile(openmwCfg, customOpenmwCfg)
            moveFile(openmwBackupCfg, openmwCfg)

        settingsCfg = self._strings.settingsCfgPath()
        settingsBackupCfg = f"{settingsCfg}.omwpbackup"
        customSettingsCfg = self._strings.customSettingsCfgPath()

        if Path(settingsCfg).exists() and Path(settingsBackupCfg).exists():
            copyFile(settingsCfg, customSettingsCfg)
            moveFile(settingsBackupCfg, settingsCfg)

        launcherCfg = self._strings.launcherCfgPath()
        launcherBackupCfg = f"{launcherCfg}.omwpbackup"
        customLauncherCfg = self._strings.customLauncherCfgPath()

        if Path(launcherCfg).exists() and Path(launcherBackupCfg).exists():
            copyFile(launcherCfg, customLauncherCfg)
            moveFile(launcherBackupCfg, launcherCfg)

