import os, shutil, hashlib, stat
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