try:
    from PyQt5.QtCore import QCoreApplication, qInfo
    from PyQt5 import QtWidgets
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
    from PyQt6 import QtWidgets
from ..rootbuilder_plugin import RootBuilderPlugin
import mobase

class RootBuilderMapperPlugin(RootBuilderPlugin, mobase.IPluginFileMapper):
    """ Main Root Builder plugin. Handles auto build features """

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.startingRootExe = False
        self.organiser.onAboutToRun(lambda appName: self.build(appName))
        self.organiser.onFinishedRun(lambda appName, resultCode: self.clear(appName, resultCode))
        self.organiser.onUserInterfaceInitialized(lambda window: self.onInitialise(window))
        return res
    
    def description(self):
        return self.__tr("Allows management of base game files by utilising a Root folder within individual mods.")

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def mappings(self):
        """ Returns mappings, if there are any, for usvfs mode. """
        return self.rootBuilder.mappings()

    def build(self, appName):
        """ Runs a build if autobuild is enabled and potentially redirects the exe being run """
        res = True
        qInfo("Building...")
        # Check if this is a secondary run from redirect.
        if (self.startingRootExe == False):
            qInfo("Starting Root Exe = False")
            # Run a build if autobuild is enabled.
            if self.rootBuilder.settings.autobuild():
                self.rootBuilder.build()
            # Possibly redirect to a different exe.
            if self.rootBuilder.settings.redirect():
                res = self.redirect(appName)
        return res

    def clear(self, appName, resultCode):
        """ Runs a clear operation if autobuild is enabled. """
        if self.rootBuilder.settings.autobuild():
            self.rootBuilder.clear()
            qInfo("Setting Root Exe = False")
            self.startingRootExe = False

    def redirect(self, appName):
        """ Redirects an app to the game path version if it is from a root mod folder. """
        # Check if the app shares a path with the mods path.
        qInfo("Redirecting")
        if self.rootBuilder.paths.sharedPath(self.rootBuilder.paths.modsPath(), appName):
            self.startingRootExe = True
            qInfo("Setting Root Exe = True")
            # Check if the exe exists in the game path.
            exeGamePath = self.rootBuilder.paths.gamePath() / self.rootBuilder.paths.rootRelativePath(appName)
            if exeGamePath.exists():
                # Run the game path version of the application.
                self.organiser.waitForApplication(self.organiser.startApplication(str(exeGamePath)))
                qInfo("Setting Root Exe = False")
                self.startingRootExe = False
                # Return false to prevent the original run.
                return False
        return True
        
    def onInitialise(self, mainWindow):
        self.rootBuilder.migrate()
        self.rootBuilder.updateFix()
        #if self.rootBuilder.updater.hasGameUpdateBug():
        #    self.updateWarning()

    def updateWarning(self):
        """ Obsolete. the fix effectively just runs, but the restore doesn't happen until the user clears and your backup/cache aren't cleared as a result. The bug only occurs if the game is actually updated while a build is still present, aka, almost never. """
        warnMsg = "<p>Your game has been updated since Root Builder last cleared. This can cause problems.</p>"
        warnMsg += "<p>Clicking OK will run Root Builder's update fix, which will do the following;</p>"
        warnMsg += "<ul>"
        warnMsg += "<li>Run a clear, restoring your game to the last version that Root Builder backed up. <b>You will need to exit Mod Organizer and re-update your game to the latest version before running a build.</b></li>"
        warnMsg += "<li>Changes since your last build, including files from the game updating, will be moved to your overwrite folder. <b>It is suggested that you clear overwrite to avoid unwanted side effects.</b></li>"
        warnMsg += "<li>Prepare to take a fresh backup and cache the next time a Root Builder builds.</li>"
        warnMsg += "</ul>"
        warnMsg += "<p>Once you run this fix, Root Builder will return to normal function.</p>"
        warnMsg += "<p>If you do not wish to run the update fix now, or wish to resolve the issue manually, click Cancel to continue to Mod Organizer.</p>"
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(warnMsg)
        msg.setWindowTitle("Root Builder Update Warning")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        res = msg.exec()
        if res == QtWidgets.QMessageBox.Ok:
            self.rootBuilder.updateFix()
        return res
