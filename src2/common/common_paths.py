import mobase, glob, os
from pathlib import Path
from typing import List

class CommonPaths:
    """Shared class containing commonly used path operations for Mod Organizer plugins."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer):
        self._organiser = organiser
        self._plugin = plugin

    def pathExists(self, path:str) -> bool:
        """Determines if a path exists, supports wildcards."""
        for match in glob.glob(path, recursive=True):
            if match != "":
                return True
        return False
    
    def pathShared(self, parentPath:str, childPath:str) -> bool:
        """Determines if the second path is a child of the first path, supports wildcards."""
        for match in glob.glob(parentPath, recursive=True):
            if self._pathShared(match, childPath):
                return True
        return False

    def _pathShared(self, parentPath:str, childPath:str) -> bool:
        """Determines if the second path is a child of the first path."""
        try:
            if os.path.commonpath([os.path.abspath(parentPath), os.path.abspath(childPath)]) == os.path.commonpath([os.path.abspath(parentPath)]):
                return True
        except:
            return False
        return False
    
    def relativePath(self, parentPath:str, childPath:str) -> str:
        """Gets the relative path for the child, relative to the parent."""
        return str(os.path.abspath(Path(childPath))).replace(str(os.path.abspath(str(parentPath))), "")[1:]
    
    def subfolders(self, path:str, recursive=True) -> List[str]:
        """Retrieves a complete collection of subfolders for the specified path."""
        res = []
        basePath = Path(path)
        for sub in os.listdir(path):
            fullPath = basePath / sub
            if Path.is_dir(fullPath):
                strPath = str(fullPath)
                res.append(strPath)
                if recursive:
                    res.extend(self.subfolders(strPath, recursive))
        return res
    
    def files(self, path:str, recursive=True) -> List[str]:
        """Retrieves a complete collection of files in the specified path."""
        basePath = Path(path)
        if recursive:
            basePath = basePath / "**" 
        basePath = basePath / "*.*"
        return glob.glob(str(basePath), recursive=True)