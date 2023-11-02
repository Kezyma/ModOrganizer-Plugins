import mobase, json, shutil, os, stat, hashlib, urllib.request, threading
from pathlib import Path

class CommonUtilities():

    def __init__(self, organiser:mobase.IOrganizer) -> None:
        self._organiser = organiser

    def copyFileOrFolder(self, source:str, dest:str) -> bool:
        """Copies a file or folder from source to destination."""
        try:
            path = Path(dest)
            if path.exists():
                if path.is_dir():
                    return self.copyFolder(source,dest)
                elif path.is_file():
                    return self.copyFile(source,dest)
            return False
        except:
            return False

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

    def copyFolder(self, source:str, dest:str) -> bool:
        """Copies a folder from source to destination."""
        try:
            shutil.copytree(source, dest, dirs_exist_ok=True)
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

    def deleteFile(self, file:str) -> bool:
        """Deletes a file."""
        try:
            if (Path(file).exists()):
                os.chmod(file, stat.S_IWRITE)
            os.remove(file)
            return True
        except:
            return False
        
    def deleteFolder(self, file:str) -> bool:
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
            os.makedirs(os.path.dirname(path), exist_ok=True)
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
        
    def loadLines(self, path:str):
        """Loads a list of lines from a file."""
        try:
            with open(path, "r") as file:
                lines = [line.rstrip() for line in file]
                return lines
        except:
            return None
        
    def saveLines(self, path:str, data:list) -> bool:
        """Saves a list of lines to a file."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(Path(path), "w", encoding="utf-8") as jsonFile:
                jsonFile.writelines(data)
                return True
        except:
            return False
        
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
    
    def downloadFile(self, url:str, path:str) -> bool:
        """Downloads a file to a specific location."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            urllib.request.urlretrieve(url, path)
            return True
        except:
            return False
        
    def folderIsEmpty(self, path:str):
        items = os.listdir(path)
        empty = True
        if len(items) > 0:
            for itm in items:
                fullPath = os.path.join(path, itm)
                if os.path.isdir(fullPath):
                    subIsEmpty = self.folderIsEmpty(fullPath)
                    empty = empty and subIsEmpty
                else:
                    empty = False
        return empty
    
    def deleteEmptyFolders(self, path:str):
        items = os.listdir(path)
        empty = True
        if len(items) > 0:
            for itm in items:
                fullPath = os.path.join(path, itm)
                if os.path.isdir(fullPath):
                    subIsEmpty = self.deleteEmptyFolders(fullPath)
                    empty = empty and subIsEmpty
                else:
                    empty = False
        if empty:
            os.rmdir(path)
        return empty

