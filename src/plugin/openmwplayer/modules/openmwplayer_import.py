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
        """Imports openmw.cfg settings.

        If the external config (user-selected or default location) exists,
        imports from there. Otherwise, imports from the bundled default config.
        Never prompts the user - they can manually select a path through the UI.
        """
        # Determine source: external config if exists, otherwise bundled default
        externalPath = self._strings.openmwCfgPath()
        if Path(externalPath).is_file():
            sourcePath = externalPath
        else:
            sourcePath = self._strings.defaultOpenmwCfgPath

        # Get destination path (custom/profile-local openmw.cfg)
        destPath = self._strings.customOpenmwCfgPath()

        # Import the config
        if Path(sourcePath).exists():
            # Delete any existing custom openmw.cfg
            if Path(destPath).exists():
                deleteFile(destPath)
            # Copy in the source config
            copyFile(sourcePath, destPath)

    def importSettingsCfg(self):
        """Imports settings.cfg from external location or default."""
        cfgPath = self._strings.settingsCfgPath()
        # If external settings.cfg doesn't exist, use downloaded default
        if not Path(cfgPath).exists():
            cfgPath = self._strings.defaultSettingsCfgPath

        # If the config exists, import it
        if Path(cfgPath).exists():
            currentPath = self._strings.customSettingsCfgPath()
            # Delete any existing settings.cfg
            if Path(currentPath).exists():
                deleteFile(currentPath)
            # Copy in the new one
            copyFile(cfgPath, currentPath)

    def exportOpenmwCfg(self):
        """Exports current settings to the external openmw.cfg location.

        Creates the target directory if it doesn't exist (handles fresh OpenMW installs).
        """
        destPath = self._strings.openmwCfgPath()
        sourcePath = self._strings.customOpenmwCfgPath()

        # Only export if we have a custom config to export
        if Path(sourcePath).exists():
            # Create target directory if needed (e.g., My Games/OpenMW may not exist)
            targetDir = Path(destPath).parent
            if not targetDir.exists():
                os.makedirs(targetDir, exist_ok=True)
            copyFile(sourcePath, destPath)

    def exportSettingsCfg(self):
        """Exports current settings.cfg to the external location."""
        destPath = self._strings.settingsCfgPath()
        sourcePath = self._strings.customSettingsCfgPath()

        if Path(sourcePath).exists():
            # Create target directory if needed
            targetDir = Path(destPath).parent
            if not targetDir.exists():
                os.makedirs(targetDir, exist_ok=True)
            copyFile(sourcePath, destPath)

    def importLauncherCfg(self):
        """Imports launcher.cfg from external location if it exists.

        Unlike settings.cfg, there is no bundled default for launcher.cfg.
        Import only happens if the external file exists.
        """
        cfgPath = self._strings.launcherCfgPath()
        # Only import if external launcher.cfg exists (no bundled default)
        if Path(cfgPath).exists():
            currentPath = self._strings.customLauncherCfgPath()
            if Path(currentPath).exists():
                deleteFile(currentPath)
            copyFile(cfgPath, currentPath)

    def exportLauncherCfg(self):
        """Exports current launcher.cfg to the external location."""
        destPath = self._strings.launcherCfgPath()
        sourcePath = self._strings.customLauncherCfgPath()

        if Path(sourcePath).exists():
            # Create target directory if needed
            targetDir = Path(destPath).parent
            if not targetDir.exists():
                os.makedirs(targetDir, exist_ok=True)
            copyFile(sourcePath, destPath)

