import mobase, os, base64, re, json, urllib, pathlib
from .modules.creationeer_paths import CreationeerPaths
from .modules.creationeer_files import CreationeerFiles
from .modules.creationeer_settings import CreationeerSettings
from ..shared.shared_utilities import SharedUtilities
from pathlib import Path
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class Creationeer():
    
    def __init__(self, organiser = mobase.IOrganizer):
        self.organiser = organiser
        self.settings = CreationeerSettings(self.organiser)
        self.paths = CreationeerPaths(self.settings, self.organiser)
        self.files = CreationeerFiles(self.settings, self.paths, self.organiser)
        self.utilities = SharedUtilities()
        self.deployInitialCache()
        super().__init__()

    fileRegex = r'data\/([A-Za-z0-9\-\_\s\(\)]+\.[a-zA-z0-9]{0,3})'
    nameRegex = r'"name":[\s]+"([^"]+)+"'
    query = 'https://api.bethesda.net/mods/ugc-workshop/list?cc_mod=true&platform=WINDOWS&number_results=99999&bundle=false'

    def deployInitialCache(self):
        """ Deploys the initial cache file, only happens on first run. """
        if Path(self.paths.initialCachePath()).exists():
            self.utilities.moveTo(self.paths.initialCachePath(), self.paths.creationNameCacheFile())

    def generateCache(self):
        cache = self.readCache()
        with urllib.request.urlopen(self.query) as r:
            dataraw = r.read()
            datadec = dataraw.decode('utf-8').encode('utf-8')
            datajson = json.loads(datadec)
            listjson = datajson["platform"]["response"]["content"]
            for itemjson in listjson:
                itemObj = {
                    "Name": itemjson["name"],
                    "Game": itemjson["product"]
                    }
                cache[itemjson["content_id"]] = itemObj
            self.saveCache(cache)

    def sort(self):
        cache = self.readCache()
        files = self.files.creationMetaFiles()
        qInfo("Found " + str(len(files)) + " meta files.")
        sourceMeta = {}
        for meta in files:
            with open(str(meta), "rb") as metaRead:
                metaData = str(metaRead.read())
                ccId = os.path.basename(str(meta)).split("-")[0]
                sourceMeta[ccId] = str(meta)
                if ccId not in cache.keys():
                    self.generateCache()
                    cache = self.readCache()
                cache[ccId]["Meta"] = os.path.basename(str(meta))
                if "Files" not in cache[ccId].keys():
                    cache[ccId]["Files"] = []
                for match in re.findall(self.fileRegex, metaData):
                    qInfo(str(metaData))
                    qInfo("\"" + str(match) + "\"")
                    preName = str(match).split(".")[0]
                    extras = self.files.findba2Files(preName)
                    if str(match) not in cache[ccId]["Files"]:
                        cache[ccId]["Files"].append(str(match))
                    if extras:
                        for ext in extras:
                            if str(ext) not in cache[ccId]["Files"]:
                                cache[ccId]["Files"].append(str(ext))
        self.saveCache(cache)
        for key in cache.keys():
            data = cache[key]
            name = str(self.settings.modNameFormat()).replace("{creation}", str(data["Name"]))
            modFolder = self.paths.modsPath() / name.strip().replace(":", " -").replace("_", "-")
            if "Files" in data.keys():
                for fileName in data["Files"]:
                    if fileName:
                        filePath = Path(self.paths.gamePath() / self.paths.gameDataDir()) / str(fileName)
                        if not filePath.exists():
                            filePath = Path(self.organiser.overwritePath()) / str(fileName)
                            if not filePath.exists():
                                modFile = self.files.findFileInMod(str(fileName))
                                if modFile:
                                    filePath = Path(modFile)
                        if filePath.exists():
                            targetPath = modFolder / str(fileName)
                            if str(filePath) != str(targetPath):
                                qInfo("Moving" + str(filePath))
                                if not modFolder.exists():
                                    os.mkdir(str(modFolder))
                                self.utilities.moveTo(filePath, targetPath)
                    
            if "Meta" in data.keys():
                if self.settings.rootBuilderSupport():
                    if key in sourceMeta.keys():
                        manifestPath = sourceMeta[key]
                        if Path(manifestPath).exists():
                            targetPath = modFolder / "Root" / "Creations" / data["Meta"]
                            if str(manifestPath) != str(targetPath):
                                if not targetPath.parent.exists():
                                    os.makedirs(str(targetPath.parent))
                                self.utilities.moveTo(manifestPath, targetPath)
                    
    def readCache(self):
        if self.paths.creationNameCacheFile().exists():
            try:
                with open(str(self.paths.creationNameCacheFile()), 'r') as r:
                    data = json.load(r)
                    return data
            except:
                pass
        return {}

    def saveCache(self, cache):
        with open(str(self.paths.creationNameCacheFile()), 'w') as r:
            json.dump(cache, r)
