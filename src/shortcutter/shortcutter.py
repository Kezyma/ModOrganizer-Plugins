import mobase, subprocess
from .modules.shortcutter_paths import ShortcutterPaths
from .modules.shortcutter_files import ShortcutterFiles
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path

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
        if instance is not "":
            args = '-i ""' + str(instance) + '""'
        args += ' -p ""' + str(profile) + '"" ""' + str(app) + '""'
        self.createShortcut(label, moPath, icon, args)

    def createShortcut(self, label=str, url=str, icon=str, args=str):
        shortcutterPath = str(Path(__file__).parent.joinpath("shortcutter.bat"))
        command = shortcutterPath + ' "' + label + '" "' + url + '" "' + icon + '" "' + args + '" > shortcutter_log.txt'
        subprocess.call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)