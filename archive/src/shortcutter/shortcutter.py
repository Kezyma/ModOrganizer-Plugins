import mobase, subprocess, os
from .modules.shortcutter_paths import ShortcutterPaths
from .modules.shortcutter_files import ShortcutterFiles
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path

try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class Shortcutter():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.paths = ShortcutterPaths(self.organiser)
        self.files = ShortcutterFiles(self.organiser)
        self.utilities = SharedUtilities()
        super().__init__()

    def create(self, label=str, profile=str, app=str, instance=str, icon=str):
        moPath = str(self.paths.modOrganizerExePath())
        args = ""
        if instance != "":
            args = '-i ""' + str(instance) + '""'
        args += ' -p ""' + str(profile) + '"" ""' + str(app) + '""'
        self.createShortcut(label, moPath, icon, args)

    def createShortcut(self, label=str, url=str, icon=str, args=str):
        qInfo("Generating desktop shortcut.")
        scBat = str(Path(__file__).parent.joinpath("shortcutter.bat"))
        scGen = f'"{scBat}" "{label}" "{url}" "{icon}" "{args}" > shortcutter_log.txt'
        qInfo("Executing command " + str(scGen))
        subprocess.call(scGen, shell=True, stdout=open(os.devnull, 'wb'))