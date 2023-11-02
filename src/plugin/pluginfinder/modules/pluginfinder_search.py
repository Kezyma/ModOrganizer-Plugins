import mobase, threading
from .pluginfinder_strings import PluginFinderStrings
from .pluginfinder_directory import PluginFinderDirectory
from ....common.common_utilities import CommonUtilities
from ....common.common_log import CommonLog
from pathlib import Path

class PluginFinderSearch():
    """Plugin Finder search module, handles search and filter of the directory."""

    def __init__(self, organiser:mobase.IOrganizer, strings:PluginFinderStrings, directory:PluginFinderDirectory, util:CommonUtilities, log:CommonLog):
        self._strings = strings
        self._util = util
        self._log = log
        self._organiser = organiser
        self._directory = directory

    def searchDirectory(self, searchTerms:str):
        directory = self._directory.loadDirectory()
        res = []
        for ix in range(len(directory)):
            dItm = directory[ix]
            if dItm[self._directory._nameKey].contains(searchTerms):
                res.append(dItm)
        return res
