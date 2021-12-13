try:
    from PyQt5.QtCore import QCoreApplication, qInfo
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
from .modules.rootbuilder_settings import RootBuilderSettings
from .modules.rootbuilder_paths import RootBuilderPaths
from .modules.rootbuilder_files import RootBuilderFiles
from .modules.rootbuilder_backup import RootBuilderBackup
from .modules.rootbuilder_mapper import RootBuilderMapper
from .modules.rootbuilder_linker import RootBuilderLinker
from .modules.rootbuilder_copy import RootBuilderCopy
from .modules.rootbuilder_update import RootBuilderUpdate

import mobase

class RootBuilder():
    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = RootBuilderSettings(self.organiser)
        self.paths = RootBuilderPaths(self.organiser)
        self.files = RootBuilderFiles(self.organiser, self.settings, self.paths)
        self.backup = RootBuilderBackup(self.organiser, self.settings, self.paths, self.files)
        self.mapper = RootBuilderMapper(self.organiser, self.settings, self.paths, self.files)
        self.linker = RootBuilderLinker(self.organiser, self.paths, self.files)
        self.copier = RootBuilderCopy(self.organiser, self.settings, self.paths, self.files, self.backup)
        self.updater = RootBuilderUpdate(self.organiser, self.paths, self.files)
        super().__init__()

    def migrate(self):
        self.updater.migrateLegacyGameData()

    def updateFix(self):
        self.updater.fixGameUpdateBug()

    def build(self):
        qInfo("Running for version " + self.backup.paths.gameVersion())
        self.updateFix()

        qInfo("RootBuilder: Starting build.")

        qInfo("RootBuilder: Backing up files.")
        self.backup.backup()
        qInfo("RootBuilder: Backed up files.")
        if self.settings.usvfsmode():
            if self.settings.linkmode():
                qInfo("RootBuilder: Generating links.")
                self.linker.build()
                qInfo("RootBuilder: Links generated.")
        else:
            qInfo("RootBuilder: Copying files.")
            self.copier.build()
            qInfo("RootBuilder: Files copied.")

        qInfo("RootBuilder: Build complete.")

    def sync(self):
        qInfo("Running for version " + self.backup.paths.gameVersion())
        self.updateFix()

        qInfo("RootBuilder: Starting sync.")
        self.copier.sync()
        qInfo("RootBuilder: Sync complete.")
        return

    def clear(self):
        qInfo("Running for version " + self.backup.paths.gameVersion())
        self.updateFix()

        qInfo("RootBuilder: Starting clear.")

        qInfo("RootBuilder: Clearing any links.")
        self.linker.clear()
        qInfo("RootBuilder: Links cleared.")

        qInfo("RootBuilder: Clearing any copied files.")
        self.copier.clear()
        qInfo("RootBuilder: Copied files cleared.")

        qInfo("RootBuilder: Restoring game files.")
        self.backup.restore()
        qInfo("RootBuilder: Game files restored.")
        
        qInfo("RootBuilder: Cleaning up overwrite.")
        self.mapper.cleanup()
        qInfo("RootBuilder: Overwrite cleaned.")

        qInfo("RootBuilder: Clear complete.")

    def mappings(self):
        return self.mapper.mappings()
        

        