import mobase, subprocess, os
from pathlib import Path
from ....common.common_log import CommonLog
from .shortcutter_settings import ShortcutterSettings
from ..modules.shortcutter_strings import ShortcutterStrings
from ..modules.shortcutter_paths import ShortcutterPaths

class Shortcutter:
    """Core Shortcutter class that handles all plugin functionality."""

    def __init__(self, organiser: mobase.IOrganizer) -> None:
        self._organiser = organiser
        self._settings = ShortcutterSettings(self._organiser)
        self._strings = ShortcutterStrings("Shortcutter", self._organiser)
        self._log = CommonLog("Shortcutter", self._settings)
        self._paths = ShortcutterPaths("Shortcutter", self._organiser, self._settings, self._strings)

    def create(self, label=str, profile=str, app=str, instance=str, icon=str):
        moPath = str(self._strings.moExecutablePath)
        args = ""
        if instance != "":
            args = '-i ""' + str(instance) + '""'
        args += ' -p ""' + str(profile) + '"" ""' + str(app) + '""'
        self.createShortcut(label, moPath, icon, args)

    def createShortcut(self, label=str, url=str, icon=str, args=str):
        self._log.info("Generating desktop shortcut.")
        scBat = str(Path(__file__).parent.parent.joinpath("util").joinpath("shortcutter.bat"))
        scGen = f'"{scBat}" "{label}" "{url}" "{icon}" "{args}" > shortcutter_log.txt'
        self._log.info("Executing command " + str(scGen))
        subprocess.call(scGen, shell=True, stdout=open(os.devnull, 'wb'))