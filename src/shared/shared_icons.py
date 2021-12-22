try:
    from PyQt5.QtGui import QIcon
except:
    from PyQt6.QtGui import QIcon
from pathlib import Path

class SharedIcons():

    def __init__(self):
        super().__init__()

    def icon(self, icon=str):
        return QIcon(str(Path(__file__).parent.joinpath("icons").joinpath(icon)))

    def checkIcon(self):
        return self.icon("ui-check.ico")

    def menuIcon(self):
        return self.icon("ui-menu.ico")

    def minusIcon(self):
        return self.icon("ui-minus.ico")

    def plusIcon(self):
        return self.icon("ui-plus.ico")

    def syncIcon(self):
        return self.icon("ui-sync.ico")

    def linkIcon(self):
        return self.icon("ui-link.ico")

    def pluginIcon(self):
        return self.icon("ui-plugin.ico")

    def nexusIcon(self):
        return self.icon("ui-nexus.ico")

    def githubIcon(self):
        return self.icon("ui-github.ico")

    def installIcon(self):
        return self.icon("ui-install.ico")

    def docsIcon(self):
        return self.icon("ui-docs.ico")

    def prevIcon(self):
        return self.icon("ui-prev.ico")

    def nextIcon(self):
        return self.icon("ui-next.ico")

    def infoIcon(self):
        return self.icon("ui-info.ico")

    def warningIcon(self):
        return self.icon("ui-warning.ico")

    def stopIcon(self):
        return self.icon("ui-stop.ico")

    def updateIcon(self):
        return self.icon("ui-update.ico")

    def updateAltIcon(self):
        return self.icon("ui-update-alt.ico")

    def noUpdateIcon(self):
        return self.icon("ui-no-update.ico")

    def refreshIcon(self):
        return self.icon("ui-refresh.ico")

    def trashIcon(self):
        return self.icon("ui-trash.ico")

    def alphaIcon(self):
        return self.icon("ui-alpha.ico")

    def betaIcon(self):
        return self.icon("ui-beta.ico")

    def gammaIcon(self):
        return self.icon("ui-gamma.ico")

    def deltaIcon(self):
        return self.icon("ui-delta.ico")

    def downloadIcon(self):
        return self.icon("ui-download.ico")

    def linkAltIcon(self):
        return self.icon("ui-link-alt.ico")

    def filterIcon(self):
        return self.icon("ui-filter.ico")

    def recycleIcon(self):
        return self.icon("ui-recycle.ico")