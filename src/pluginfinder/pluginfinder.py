import mobase, json, urllib.request, zipfile, os, shutil, re
from .modules.pluginfinder_search import PluginFinderSearch
from ..shared.shared_utilities import SharedUtilities
from .modules.pluginfinder_paths import PluginFinderPaths
from .modules.pluginfinder_files import PluginFinderFiles
from .modules.pluginfinder_installer import PluginFinderInstaller
from pathlib import Path
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

# TODO: Check for updates function to get all installed plugins again and check if the version has changed. 
# TODO: Search function to filter plugins by text
# TODO: Uninstall needs to check for pluginData[plugin]["Data"] and remove those files/folders as well, if any exist.
# TODO: Restart Mod Organizer if a plugin has been installed.

# Retrieve the plugin manifest json only for plugins on the current page.
# Add paging system in place of the scrollbar.
# Add a search box at the top that filters based on the name in the central json file.
# Actually delete files in the DataFiles field on uninstall.
# Add version checking to see if plugins need updating and display current + new version.
# Restart ModOrganizer when PF is closed after a plugin was installed or uninstalled.

class PluginFinder():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.files = PluginFinderFiles(self.organiser)
        self.paths = PluginFinderPaths(self.organiser)
        self.installer = PluginFinderInstaller(self.organiser, self.paths, self.files)
        self.search = PluginFinderSearch(self.organiser, self.paths, self.files, self.installer)
        self.utilities = SharedUtilities()
        super().__init__()
        
    def install(self, pluginId=str):
        """ Installs the latest available version of a plugin. """
        qInfo("Installing " + pluginId)
        pluginData = self.search.pluginData(pluginId)
        self.installer.installPlugin(pluginData)

    def uninstall(self, pluginId=str):
        """ Uninstalls the current version of a plugin. """
        qInfo("Uninstalling " + pluginId)
        self.installer.uninstallPlugin(pluginId)

    def initial(self, pfVersion=str):
        self.search.deployInitialDirectory()
        if self.installer.initialInstall(pfVersion):
            self.search.increaseInstallCount("pluginfinder")