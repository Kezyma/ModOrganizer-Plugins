import mobase, json, shutil, os, stat, hashlib
from pathlib import Path

class CommonUtilities():

    def __init__(self, organiser:mobase.IOrganizer) -> None:
        self._organiser = organiser

    def copyFile(self, source:str, dest:str) -> bool:
        """Copies a file from source to destination."""
        try:
            if (Path(dest).exists()):
                os.chmod(dest, stat.S_IWRITE)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(source, dest)
            return True
        except:
            return False

    def moveFile(self, source:str, dest:str) -> bool:
        """Moves a file from source to destination."""
        try:
            if (Path(dest).exists()):
                os.chmod(dest, stat.S_IWRITE)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(str(source), str(dest))
            return True
        except:
            return False

    def deleteFile(self, file=str) -> bool:
        """Deletes a file."""
        try:
            if (Path(file).exists()):
                os.chmod(file, stat.S_IWRITE)
            os.remove(file)
            return True
        except:
            return False
        
    def deleteFolder(self, file=str) -> bool:
        """Deletes a folder."""
        try:
            if Path(file).exists():
                shutil.rmtree(file)
            return True
        except:
            return False

    def linkFile(self, source:str, dest:str) -> bool:
        """Links a file to a specific location."""
        try:
            Path(source).link_to(dest)
            return True
        except:
            return False

    def unlinkFile(self, link:str) -> bool:
        """Unlinks a file."""
        try:
            Path(link).unlink()
            return True
        except:
            return False

    def saveJson(self, path:str, data) -> bool:
        """Saves an object to a json file."""
        try:
            with open(Path(path), "w", encoding="utf-8") as jsonFile:
                json.dump(data, jsonFile)
                return True
        except:
            return False
        
    def loadJson(self, path:str):
        """Loads an object from a json file."""
        try:
            return json.load(open(Path(path),"r", encoding="utf-8"))
        except:
            return None
        
    def hashFile(self, path:str) -> str:
        """ Hashes a file and returns the hash """
        func = hashlib.md5()
        if (Path(path).exists()):
            os.chmod(path, stat.S_IWRITE)
        f = os.open(path, (os.O_RDONLY | os.O_BINARY))
        for block in iter(lambda: os.read(f, 2048*func.block_size), b''):
            func.update(block)
        os.close(f)
        return func.hexdigest()