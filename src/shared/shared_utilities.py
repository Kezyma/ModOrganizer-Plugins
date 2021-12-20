import os, shutil, hashlib, stat, re, mobase
from shutil import copy2
from pathlib import Path
try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo

class SharedUtilities():

    def __init__(self):
        super().__init__()

    def copyTo(self, fromPath=Path, toPath=Path):
        try:
            if (Path(toPath).exists()):
                os.chmod(toPath, stat.S_IWRITE)
            os.makedirs(os.path.dirname(toPath), exist_ok=True)
            copy2(fromPath, toPath)
        except:
            qInfo("Could not copy " + str(fromPath) + " to " + str(toPath))

    def replaceDir(self, fromPath=Path, toPath=Path):
        try:
            if (Path(toPath).exists()):
                shutil.rmtree(toPath)
            shutil.copytree(fromPath, toPath)
        except:
            qInfo("Could not replace " + str(toPath) + " with " + str(fromPath))

    def deletePath(self, path=Path):
        try:
            if (Path(path).exists()):
                os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        except:
            qInfo("Could not delete " + str(path))

    def moveTo(self, fromPath=Path, toPath=Path):
        try:
            if (Path(toPath).exists()):
                os.chmod(toPath, stat.S_IWRITE)
            os.makedirs(os.path.dirname(toPath), exist_ok=True)
            shutil.move(str(fromPath), str(toPath))
        except:
            qInfo("Could not move " + str(fromPath) + " to " + str(toPath))

    def hashFile(self, path):
        """ Hashes a file and returns the hash """
        func = getattr(hashlib, 'md5')()
        if (Path(path).exists()):
            os.chmod(path, stat.S_IWRITE)
        f = os.open(path, (os.O_RDWR | os.O_BINARY))
        for block in iter(lambda: os.read(f, 2048*func.block_size), b''):
            func.update(block)
        os.close(f)
        return func.hexdigest()

    def versionIsNewer(self, oldVersion=str, newVersion=str):
        """ Works out if newVersion is newer than oldVersion. """
        oldVer = self.parseVersion(oldVersion)
        newVer = self.parseVersion(newVersion)
        return newVer > oldVer
    
    def parseVersion(self, version=str):
        """ Parses a version. """
        return mobase.VersionInfo(version)

    alphaStrings = [ "a", "alpha" ]
    betaStrings = [ "b", "beta" ]
    rcStrings = [ "g", "rc", "candidate" ]

    def betaVersion(self, version=str):
        for bs in self.betaStrings:
            if bs in str(version).lower():
                return True
        return False

    def alphaVersion(self, version=str):
        for asS in self.alphaStrings:
            if asS in str(version).lower():
                return True
        return False

    def rcVersion(self, version=str):
        for rs in self.rcStrings:
            if rs in str(version).lower():
                return True
        return False