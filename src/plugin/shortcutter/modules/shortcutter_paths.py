import mobase, glob, re
from pathlib import Path
from .shortcutter_strings import ShortcutterStrings
from ..core.shortcutter_settings import ShortcutterSettings
from ....common.common_paths import CommonPaths
from ....common.common_log import CommonLog
from typing import List

class ShortcutterPaths(CommonPaths):
    """Shortcutter paths module, contains path related functions for Root Builder."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:ShortcutterSettings, strings:ShortcutterStrings):
        super().__init__(plugin, organiser)
        self._strings = strings
        self._settings = settings

    def modOrganizerApps(self):
        return self.modOrganizerAppPaths().keys()

    def modOrganizerAppPaths(self):
        paths = {}
        names = {}
        with open(self._strings.moIniPath) as ini:
            for line in ini:
                txt = line.rstrip()
                parts = txt.split("\\")
                if len(parts) > 1:
                    appId = parts[0]
                    part = parts[1].split("=")
                    if part[0] == "title":
                        names[appId] = part[1]
                    if part[0] == "binary":
                        paths[appId] = part[1]
        res = {}
        for appId in names.keys():
            res[names[appId]] = paths[appId]
        return res