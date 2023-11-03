import mobase
from pathlib import Path
from ..core.rootbuilder_settings import RootBuilderSettings
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog

class RootBuilderLegacy():
    """Root Builder legacy module, handles migration from old versions."""

    def __init__(self, organiser:mobase.IOrganizer,settings:RootBuilderSettings,utilities:CommonUtilities,log:CommonLog):
        self._organiser = organiser
        self._util = utilities
        self._log = log
        self._settings = settings

    def migrate(self):
        migrated = self._settings.migrated()
        if not migrated:
            # Update the settings to work with the new modes.
            linkMode = self._settings.linkmode()
            linkOnlyMode = self._settings.linkonlymode()
            usvfsMode = self._settings.usvfsmode()
            linkExt = self._settings.linkextensions()
            copyMode = not linkMode and not usvfsMode and not linkOnlyMode
            if copyMode:
                self._organiser.setPluginSetting("RootBuilder", "copyfiles", "**")
                self._organiser.setPluginSetting("RootBuilder", "linkfiles", "")
                self._organiser.setPluginSetting("RootBuilder", "usvfsfiles", "")
            elif linkOnlyMode:
                self._organiser.setPluginSetting("RootBuilder", "copyfiles", "")
                self._organiser.setPluginSetting("RootBuilder", "linkfiles", "**")
                self._organiser.setPluginSetting("RootBuilder", "usvfsfiles", "")
            elif usvfsMode:
                self._organiser.setPluginSetting("RootBuilder", "copyfiles", "")
                self._organiser.setPluginSetting("RootBuilder", "usvfsfiles", "**")
                linkExtStr = []
                for ext in linkExt:
                    linkExtStr.append("**\\*." + ext)
                self._organiser.setPluginSetting("RootBuilder", "linkfiles", ",".join(linkExtStr))

            # Update exclusions now that data isn't excluded by default.
            exclusion = self._settings.exclusions()
            exclusion.append("Data")
            exclusion.append("Data Files")
            self._organiser.setPluginSetting("RootBuilder", "exclusions", ",".join(exclusion))

            # Set the Hash setting to whatever the Cache setting is.
            cache = self._settings.cache()
            self._organiser.setPluginSetting("RootBuilder", "hash", cache)

            # Mark this whole thing as migrated.
            self._organiser.setPluginSetting("RootBuilder", "migrated", True)