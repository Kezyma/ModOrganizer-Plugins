import mobase, os
from pathlib import Path
from os import listdir

class SharedFiles():

    def __init__(self, pluginName = str, organiser=mobase.IOrganizer):
        self.pluginName = pluginName
        self.organiser = organiser
        super().__init__()

    def getFolderFileList(self, path):
        """ Lists all files in a folder, including all subfolders """
        res = []   
        # Grab the full contents of the folder.
        for fp in listdir(path):
            afp = Path(path) / fp
            # If the content is a file, add it to the list.
            if (Path.is_file(afp)):
                res.append(afp)
            # If the content is a folder, load the contents.
            if (Path.is_dir(afp)):
                res.extend(self.getFolderFileList(afp))
        return res

    def getSubFolderList(self, path, recursive=True):
        """ Lists all folders in a folder, including all subfolders """
        res = []   
        # Grab the full contents of the folder.
        for fp in listdir(path):
            afp = Path(path) / fp
            # If the content is a folder, add it and load subfolders.
            if (Path.is_dir(afp)):
                res.append(afp)
                if (recursive):
                    res.extend(self.getSubFolderList(afp, recursive))
        return res

    def getFileNamesFromList(self, list):
        files = []
        for item in list:
            files.append(os.path.basename(str(item)))
        return files

    
    def modOrganizerExecutables(self):
        """ Gets the list of executables from Mod Organizer. """
        titles = []
        for executable in self.organiser.managedGame().executables():
            titles.append(executable.title())
        return titles

