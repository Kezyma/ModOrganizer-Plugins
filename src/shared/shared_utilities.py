import os, shutil, hashlib, stat, re
from shutil import copy2
from pathlib import Path

class SharedUtilities():

    def __init__(self):
        super().__init__()

    def copyTo(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            os.chmod(toPath, stat.S_IWRITE)
        os.makedirs(os.path.dirname(toPath), exist_ok=True)
        copy2(fromPath, toPath)

    def replaceDir(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            shutil.rmtree(toPath)
        shutil.copytree(fromPath, toPath)

    def deletePath(self, path=Path):
        if (Path(path).exists()):
            os.chmod(path, stat.S_IWRITE)
        os.remove(path)

    def moveTo(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            os.chmod(toPath, stat.S_IWRITE)
        os.makedirs(os.path.dirname(toPath), exist_ok=True)
        shutil.move(str(fromPath), str(toPath))

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
        
        parts = max(len(oldVer),len(newVer))
        for i in range(parts):
            oldPart = "0"
            newPart = "0"
            if len(oldVer) > i:
                oldPart = oldVer[i]
            if len(newVer) > i:
                newPart = newVer[i]
            try: # numeric sorting, for the version number itself.
                oldInt = int(oldPart)
                newInt = int(newPart)
                if newInt > oldInt:
                    return True
                if newInt < oldInt:
                    return False
            except: # alphabetic string sorting. useful for picking in order for alpha and beta releases.
                if newPart < oldPart:
                    return True 
                if newPart > oldPart:
                    return False
        return False
    
    def parseVersion(self, version=str):
        """ Splits up a version string. """
        ver = []
        for part in str(version).split("."):
            numPart = "".join(filter(str.isdigit, part))
            txtPart = "".join(filter(!str.isdigit, part))
            if numPart != "":
                ver.append(numPart)
            if txtPart != "":
                ver.append(txtPart)
        return ver