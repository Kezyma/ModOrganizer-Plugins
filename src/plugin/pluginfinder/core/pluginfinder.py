import mobase
from ....common.common_log import CommonLog
from ....common.common_utilities import CommonUtilities
from ....common.common_paths import CommonPaths
from .pluginfinder_settings import PluginFinderSettings
from ..modules.pluginfinder_search import PluginFinderSearch
from ..modules.pluginfinder_directory import PluginFinderDirectory
from ..modules.pluginfinder_install import PluginFinderInstall
from ..modules.pluginfinder_strings import PluginFinderStrings

class PluginFinder():
    """Core Plugin Finder class."""

    def __init__(self, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._settings = PluginFinderSettings(self._organiser)
        self._log = CommonLog("PluginFinder", self._organiser, self._settings)
        self._util = CommonUtilities(self._organiser)
        self._paths = CommonPaths("PluginFinder", self._organiser)
        self._strings = PluginFinderStrings("PluginFinder", self._organiser)
        self._directory = PluginFinderDirectory(self._organiser, self._strings, self._util, self._log)
        self._install = PluginFinderInstall(self._organiser, self._strings, self._directory, self._paths, self._util, self._log)
        self._search = PluginFinderSearch(self._organiser, self._strings, self._directory, self._install, self._util, self._log)
        super().__init__()