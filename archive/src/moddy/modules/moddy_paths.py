import mobase
from ...shared.shared_paths import SharedPaths
from .moddy_settings import ModdySettings
from pathlib import Path
try:
    from PyQt5.QtCore import QCoreApplication, QStandardPaths
    from PyQt5.QtWidgets import QFileDialog
except:
    from PyQt6.QtCore import QCoreApplication, QStandardPaths
    from PyQt6.QtWidgets import QFileDialog
import os

class ModdyPaths(SharedPaths):
    """ OpenMW Player path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer,settings=ModdySettings):
        self.settings = settings
        super().__init__("Moddy", organiser) 

    def overwritePath(self):
        return self.organiser.overwritePath()