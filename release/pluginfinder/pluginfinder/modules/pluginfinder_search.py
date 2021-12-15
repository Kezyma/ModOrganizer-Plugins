import mobase, os, urllib, json, math, shutil, re
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
            for item in self.directory():
                self.refreshPluginCount(item["Identifier"])

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

        for item in self.directory():
            self.refreshPluginCount(item["Identifier"])

    def directory(self):
        """ Get the directory as json. """
        # If the file is missing or old, update it.
        directoryJsonPath = self.paths.directoryJsonPath()
        if not Path(directoryJsonPath).exists() or datetime.fromtimestamp(os.path.getmtime(str(directoryJsonPath))) < (datetime.today() - timedelta(days=1)):
            self.updateDirectory()
        # Load the directory file.
        directory = json.load(open(directoryJsonPath))
        return directory

    def searchDirectory(self, searchTerms=str, installed=False):
        """ Searches the directory by plugin name. """
        plugins = []
        directory = self.directory()
        counters = self.loadCounters()
        countless = []
        counted = []
        for item in directory:
            try:
                if item["Identifier"] not in counters:
                    self.refreshPluginCount(item["Identifier"])
                dl = int(str(counters[item["Identifier"]]["Downloads"]))
                counted.append(item)
            except:
                countless.append(item)
        
        counted = sorted(counted, key=lambda p: int(str(counters[p["Identifier"]]["Downloads"])), reverse=True)
        directory = counted + countless

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
                if searchTerms.lower() in plugin["Name"].lower():
                    results.append(plugin)
        return results

    def updatePluginData(self, pluginId=str):
        """ Gets the json file for the current plugin. """
        for plugin in self.directory():
            if str(plugin["Identifier"]) == str(pluginId):
                if "Manifest" in plugin:
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
                if "Name" not in data:
                    data["Name"] = self.directoryEntryById(pluginId)["Name"]
                return PluginData(data)
            except:
                qInfo("Could not load plugin " + self.directoryEntryById(pluginId)["Name"])
        # Return an null if we can't load the file.
        return PluginData(self.directoryEntryById(pluginId))

    def directoryEntryById(self, pluginId = str):
        """ Gets an entry from the directory using a plugin id. """
        directory = self.directory()
        for plugin in directory:
            if plugin["Identifier"] == pluginId:
                return plugin

    def pagedPluginData(self, searchTerms=str, installed=False, page=int, pageSize=int):
        """ Get a paged list of plugin data. """
        qInfo("Searching directory, terms = " + str(searchTerms) + " installed = " + str(installed))
        manifestSearch = self.searchDirectory(searchTerms, installed)
        totalItems = int(math.ceil(float(len(manifestSearch)) / pageSize))
        qInfo("Directory searched, paging list.")
        pagedList = list(islice(manifestSearch, ((page-1)*pageSize), ((page-1)*pageSize) + pageSize))
        qInfo("List paged, loading plugin data.")
        results = []
        for item in pagedList:
            if "Identifier" in item.keys():
                results.append(self.pluginData(str(item["Identifier"])))
        qInfo("Plugin data loaded.")
        return results, totalItems

    def totalPages(self, searchTerms=str, installed=False, pageSize=int):
        """ Gets the total number of pages from a search. """
        items = float(len(self.searchDirectory(searchTerms, installed)))
        return int(math.ceil(items / pageSize))

    def refreshData(self):
        self.updateDirectory()
        shutil.rmtree(self.paths.pluginDataCacheFolderPath())

    def buildInitialCache(self):
        """ Gets json data for every plugin. """
        for plugin in self.directory():
            self.pluginData(plugin["Identifier"])

    def getGithubReleaseJson(self, author=str, repo=str, tag=str):
        endpointUrl = "https://api.github.com/repos/" + author + "/" + repo + "/releases/tags/" + tag
        # Load cache if it exists and is recent.
        cacheName = self.paths.githubReleaseJsonCachePath(author, repo, tag)
        if Path(cacheName).exists() and datetime.fromtimestamp(os.path.getmtime(str(cacheName))) > (datetime.today() - timedelta(days=1)):
            return json.load(open(cacheName))
        # Load the data otherwise.
        request = urllib.request.Request(endpointUrl)
        request.add_header("Accept", "application/vnd.github.v3+json")
        with urllib.request.urlopen(request) as r:
            data = json.load(r)
            if not Path(cacheName).exists():
                Path(cacheName).touch()
            with open(cacheName, "w") as rcJson:
                json.dump(data, rcJson)
            return data

    def getGithubDownloadCount(self, author=str, repo=str, tag=str, zipName=str):
        releaseJson = self.getGithubReleaseJson(author, repo, tag)
        if "assets" in releaseJson:
            assets = releaseJson["assets"]
            for asset in assets:
                if asset["browser_download_url"].endswith(zipName):
                    count = int(asset["download_count"])
                    return int(count)
        return None

    downloadUrlRegex = r"https:\/\/github.com\/([^\/]*)\/([^\/]*)\/releases\/download\/([^\/]*)\/([^\/]*)"

    def getTotalGithubDownloadCount(self, data=PluginData):
        counters = self.loadCounters()
        plugin = data.identifier()

        if plugin in counters:
            updated = datetime.fromisoformat(counters[plugin]["Updated"])
            if updated > (datetime.today() - timedelta(days=1)):
                return int(counters[plugin]["Downloads"])
        else:
            counters[plugin] = { }
            counters[plugin]["Updated"] = datetime.today().isoformat()
            counters[plugin]["Downloads"] = "?"
        
        total = 0
        if data.versions():
        #try:
            for version in data.versions():
                    match = re.match(self.downloadUrlRegex, version.downloadUrl())
                    if match:
                        author = match.groups()[0]
                        repo = match.groups()[1]
                        tag = match.groups()[2]
                        name  = match.groups()[3]
                        total += self.getGithubDownloadCount(author, repo, tag, name)
            counters[plugin]["Downloads"] = str(total)
            self.saveCounters(counters)
            return total
        #except:
        #    qInfo("Could not load download counter for " + str(plugin))
        return None

    def loadCounters(self):
        if self.paths.counterJsonPath().exists():
            fileData = json.load(open(self.paths.counterJsonPath()))
            return fileData
        return {}

    def saveCounters(self, counters):
        if not self.paths.counterJsonPath().exists():
            self.paths.counterJsonPath().touch()
        with open(self.paths.counterJsonPath(), "w") as rcJson:
            json.dump(counters, rcJson)

    def tryCreateInstallCount(self, pluginId=str):
        # Create a counter if it doesn't exist.
        createUrl = "https://api.countapi.xyz/create?key=" + pluginId + "&namespace=pluginfinder&value=0"
        try:
            urllib.request.urlopen(createUrl)
        except:
            pass

    def refreshPluginCount(self, pluginId=str):
        counters = self.loadCounters()
        if pluginId not in counters:
            counters[pluginId] = { }
        counters[pluginId]["Updated"] = datetime.today().isoformat()
        counters[pluginId]["Downloads"] = "?"
        self.tryCreateInstallCount(pluginId)
        url = "https://api.countapi.xyz/get/pluginfinder/" + str(pluginId)
        try:
            with urllib.request.urlopen(url) as r:
                data = json.load(r)
                val = data["value"]
                counters[pluginId]["Downloads"] = str(val)
        except: 
            counters[pluginId]["Downloads"] = "?"
        self.saveCounters(counters)
        return str(counters[pluginId]["Downloads"])

    def getInstallCount(self, pluginId=str):
        counters = self.loadCounters()
        if pluginId in counters:
            updated = datetime.fromisoformat(counters[pluginId]["Updated"])
            if updated > (datetime.today() - timedelta(hours=1)):
                return counters[pluginId]["Downloads"]
        return self.refreshPluginCount(pluginId)

    def increaseInstallCount(self, pluginId=str):
        self.tryCreateInstallCount(pluginId)
        url = "https://api.countapi.xyz/update/pluginfinder/" + str(pluginId) + "?amount=1"
        try:
            with urllib.request.urlopen(url) as r:
                data = json.load(r)
                val = data["value"]
                self.refreshPluginCount(pluginId)
                return str(val)
        except: 
            return "?"

    def decreaseInstallCount(self, pluginId=str):
        self.tryCreateInstallCount(pluginId)
        url = "https://api.countapi.xyz/update/pluginfinder/" + str(pluginId) + "?amount=-1"
        try:
            with urllib.request.urlopen(url) as r:
                data = json.load(r)
                val = data["value"]
                self.refreshPluginCount(pluginId)
                return str(val)
        except: 
            return "?"
