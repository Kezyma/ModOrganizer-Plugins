import mobase, os, urllib, json, math, shutil
from pathlib import Path
from datetime import datetime, timedelta
from itertools import islice
from .pluginfinder_paths import PluginFinderPaths
from .pluginfinder_files import PluginFinderFiles
from .pluginfinder_installer import PluginFinderInstaller
from ...shared.shared_utilities import SharedUtilities
from ..models.plugin_data import PluginData
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class PluginFinderSearch():

    def __init__(self, organiser=mobase.IOrganizer, paths=PluginFinderPaths, files=PluginFinderFiles, installer=PluginFinderInstaller):
        self.organiser = organiser
        self.paths = paths
        self.files = files
        self.installer = installer
        self.utilities = SharedUtilities()
        super().__init__() 

    def deployInitialDirectory(self):
        """ Deploys the initial directory file, only happens on first run. """
        if Path(self.paths.initialDirectoryPath()).exists():
            self.utilities.moveTo(self.paths.initialDirectoryPath(), self.paths.directoryJsonPath())

    def updateDirectory(self):
        """ Attempt to download a directory update from Github. """
        try:
            with urllib.request.urlopen(self.paths.pluginDirectoryUrl()) as r:
                data = json.load(r)
                if not Path(self.paths.directoryJsonPath()).exists():
                    Path(self.paths.directoryJsonPath()).touch()
                with open(self.paths.directoryJsonPath(), "w") as rcJson:
                    json.dump(data, rcJson)
        except:
            qInfo("Could not download update.")
        urllib.request.urlcleanup()

    def directory(self):
        """ Get the directory as json. """
        # Deploy if it's first run.
        self.deployInitialDirectory()
        # If the file is missing or old, update it.
        if not Path(self.paths.directoryJsonPath()).exists() or datetime.fromtimestamp(os.path.getmtime(str(self.paths.directoryJsonPath()))) < (datetime.today() - timedelta(days=1)):
            self.updateDirectory()
        # Load the directory file.
        directory = json.load(open(self.paths.directoryJsonPath()))
        return directory

    def searchDirectory(self, searchTerms=str, installed=False):
        """ Searches the directory by plugin name. """
        qInfo("Searching directory, terms = " + str(searchTerms) + " installed = " + str(installed))
        plugins = []
        directory = self.directory()
        if installed:
            for plugin in directory:
                if plugin["Identifier"] in self.installer.installedPlugins():
                    plugins.append(plugin)
        else:
            plugins = directory
            
        if searchTerms == "":
            return plugins
        results = []
        for plugin in plugins:
            if "Name" in plugin.keys():
                if searchTerms in plugin["Name"]:
                    results.append(plugin)
        return results

    def updatePluginData(self, pluginId=str):
        """ Gets the json file for the current plugin. """
        for plugin in self.directory():
            if str(plugin["Identifier"]) == str(pluginId):
                url = plugin["Manifest"]
                try:
                    with urllib.request.urlopen(str(url)) as r:
                        data = json.load(r)
                        if not Path(self.paths.pluginDataCachePath(pluginId)).exists():
                            Path(self.paths.pluginDataCachePath(pluginId)).touch()
                        with open(self.paths.pluginDataCachePath(pluginId), "w") as rcJson:
                            json.dump(data, rcJson)
                except:
                    qInfo("Could not download update.")
                urllib.request.urlcleanup()

    def pluginData(self, pluginId=str):
        """ Loads the data for a plugin. """
        # If the file is missing or old, update it.
        if not Path(self.paths.pluginDataCachePath(pluginId)).exists() or datetime.fromtimestamp(os.path.getmtime(str(self.paths.pluginDataCachePath(pluginId)))) < (datetime.today() - timedelta(days=1)):
            self.updatePluginData(pluginId)
        # If the file now exists (it should), load it.
        if Path(self.paths.pluginDataCachePath(pluginId)).exists():
            try:
                data = json.load(open(self.paths.pluginDataCachePath(pluginId)))
                data["Identifier"] = str(pluginId)
                return PluginData(data)
            except:
                return None
        # Return an null if we can't load the file.
        return None

    def pagedPluginData(self, searchTerms=str, installed=False, page=int, pageSize=int):
        """ Get a paged list of plugin data. """
        manifestSearch = self.searchDirectory(searchTerms, installed)
        qInfo("Directory searched, paging list.")
        pagedList = list(islice(manifestSearch, ((page-1)*pageSize), ((page-1)*pageSize) + pageSize))
        qInfo("List paged, loading plugin data.")
        results = []
        for item in pagedList:
            if "Identifier" in item.keys():
                results.append(self.pluginData(str(item["Identifier"])))
        return results

    def totalPages(self, searchTerms=str, installed=False, pageSize=int):
        """ Gets the total number of pages from a search. """
        items = float(len(self.searchDirectory(searchTerms, installed)))
        return int(math.ceil(items / pageSize))

    def refreshData(self):
        self.updateDirectory()
        shutil.rmtree(self.paths.pluginDataCacheFolderPath())
