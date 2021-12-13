import mobase, os, urllib, json, math
from pathlib import Path
from datetime import datetime, timedelta
from itertools import islice
from .pluginfinder_paths import PluginFinderPaths
from .pluginfinder_files import PluginFinderFiles
from ...shared.shared_utilities import SharedUtilities
from ..models.plugin_data import PluginData
from PyQt5.QtCore import QCoreApplication, qInfo

class PluginFinderInstaller():

    def __init__(self, organiser=mobase.IOrganizer, paths=PluginFinderPaths, files=PluginFinderFiles):
        self.organiser = organiser
        self.paths = paths
        self.files = files
        self.utilities = SharedUtilities()
        super().__init__() 

    def installPlugin(self, plugin=PluginData):
        currentVersion = plugin.current(self.organiser.appVersion().canonicalString())

        # Get current supported version.
        # Check 