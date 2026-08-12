import hashlib
import json
import os
import shutil
import stat
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable, Union

# Backwards compatibility: Path.link_to was deprecated in 3.10, removed in 3.12
if sys.version_info[0] >= 3 and sys.version_info[1] < 10:

    def hardlink(source: Union[str, Path], target: Union[str, Path]):
        Path(source).link_to(target)

else:

    def hardlink(source: Union[str, Path], target: Union[str, Path]):
        Path(target).hardlink_to(source)


def maxRetries():
    return 10

def copyFileOrFolder(source: str, dest: str, retries: int = 0) -> bool:
    """Copies a file or folder from source to destination."""
    try:
        path = Path(dest)
        if path.exists():
            if path.is_dir():
                return copyFolder(source, dest)
            elif path.is_file():
                return copyFile(source, dest)
        return False
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return copyFileOrFolder(source, dest, retries + 1)
        return False

def copyFile(source: str, dest: str, retries: int = 0) -> bool:
    """Copies a file from source to destination."""
    try:
        if Path(dest).exists():
            os.chmod(dest, stat.S_IWRITE)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(source, dest)
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return copyFile(source, dest, retries + 1)
        return False

def copyFolder(source: str, dest: str, retries: int = 0) -> bool:
    """Copies a folder from source to destination."""
    try:
        shutil.copytree(source, dest, dirs_exist_ok=True)
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return copyFolder(source, dest, retries + 1)
        return False

def moveFile(source: str, dest: str, retries: int = 0) -> bool:
    """Moves a file from source to destination."""
    try:
        if Path(dest).exists():
            os.chmod(dest, stat.S_IWRITE)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(str(source), str(dest))
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return moveFile(source, dest, retries + 1)
        return False

def deleteFile(file: str, retries: int = 0) -> bool:
    """Deletes a file."""
    try:
        if Path(file).exists():
            os.chmod(file, stat.S_IWRITE)
        os.remove(file)
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return deleteFile(file, retries + 1)
        return False

def deleteFolder(file: str, retries: int = 0) -> bool:
    """Deletes a folder."""
    try:
        if Path(file).exists():
            shutil.rmtree(file)
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return deleteFolder(file, retries + 1)
        return False

def linkFile(source: str, dest: str, retries: int = 0) -> bool:
    """Links a file to a specific location."""
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        hardlink(source, dest)
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return linkFile(source, dest, retries + 1)
        return False

def unlinkFile(link: str, retries: int = 0) -> bool:
    """Unlinks a file."""
    try:
        Path(link).unlink()
        return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return unlinkFile(link, retries + 1)
        return False

def saveJson(path: str, data: Any, retries: int = 0) -> bool:
    """Saves an object to a json file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(Path(path), "w", encoding="utf-8") as jsonFile:
            json.dump(data, jsonFile)
            return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return saveJson(path, data, retries + 1)
        return False

def loadJson(path: str, retries: int = 0) -> Union[Any, None]:
    """Loads an object from a json file."""
    try:
        with open(Path(path), "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return loadJson(path, retries + 1)
        return None

def loadLines(path: str, retries: int = 0) -> Union["list[str]", None]:
    """Loads a list of lines from a file."""
    try:
        with open(path, "r", encoding="utf-8-sig") as file:
            lines = [line.rstrip() for line in file]
            return lines
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return loadLines(path, retries + 1)
        return None

def saveLines(path: str, data: Iterable[str], retries: int = 0) -> bool:
    """Saves a list of lines to a file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(Path(path), "w", encoding="utf-8") as jsonFile:
            jsonFile.writelines(data)
            return True
    except OSError:
        if retries <= maxRetries():
            time.sleep(0.1)
            return saveLines(path, data, retries + 1)
        return False

def hashFile(path: str) -> str:
    """Hashes a file and returns the hash"""
    func = hashlib.md5()
    if Path(path).exists():
        os.chmod(path, stat.S_IWRITE)
    f = os.open(path, (os.O_RDONLY | os.O_BINARY))
    for block in iter(lambda: os.read(f, 2048 * func.block_size), b""):
        func.update(block)
    os.close(f)
    return func.hexdigest()

def downloadFile(url: str, path: str, retries: int = 0) -> bool:
    """Downloads a file to a specific location."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)
        return True
    except (
        OSError,
        urllib.error.URLError,
        urllib.error.HTTPError,
        urllib.error.ContentTooShortError,
    ):
        if retries <= maxRetries():
            time.sleep(0.1)
            return downloadFile(url, path, retries + 1)
        return False

def folderIsEmpty(path: str) -> bool:
    items = os.listdir(path)
    empty = True
    if len(items) > 0:
        for itm in items:
            fullPath = os.path.join(path, itm)
            if os.path.isdir(fullPath):
                subIsEmpty = folderIsEmpty(fullPath)
                empty = empty and subIsEmpty
            else:
                return False
    return empty

def deleteEmptyFolders(path: str):
    path = Path(path)
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            subdir = path / dirpath / dirname
            with os.scandir(path) as it:
                if not any(it):
                    os.rmdir(subdir)
