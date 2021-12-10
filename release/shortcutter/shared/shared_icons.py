from PyQt5.QtGui import QIcon
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