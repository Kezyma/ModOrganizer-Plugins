import mobase, webbrowser
from pathlib import Path
from .common_strings import CommonStrings
from .common_utilities import downloadFile, loadJson
from .common_icons import * 
from .common_qt import *
from .common_log import CommonLog
try:
    from ..base.ui.qt6.help_widget import Ui_helpTabWidget
except:
    from ..base.ui.qt5.help_widget import Ui_helpTabWidget

class CommonHelp:
    """Plugin help module, used to configure help tabs."""

    def __init__(self, htmlPath:Path, pluginName:str, nexusGame:str, nexusId:str, strings: CommonStrings, log: CommonLog) -> None:
        self._docsPath = htmlPath
        self._plugin = pluginName
        self._game = nexusGame
        self._nexusId = nexusId
        self._strings = strings
        self._log = log
        
    def configure(self, widget:Ui_helpTabWidget):
        self._widget = widget
        self._widget.discordButton.setIcon(DISCORD_ICON)
        self._widget.discordButton.clicked.connect(self.discord_clicked)
        self._widget.docsButton.setIcon(DOCS_ICON)
        self._widget.docsButton.clicked.connect(self.docs_clicked)
        self._widget.githubButton.setIcon(GITHUB_ICON)
        self._widget.githubButton.clicked.connect(self.github_clicked)
        self._widget.nexusButton.setIcon(NEXUS_ICON)
        self._widget.nexusButton.clicked.connect(self.nexus_clicked)
        self._widget.patreonButton.setIcon(PATREON_ICON)
        self._widget.patreonButton.clicked.connect(self.patreon_clicked)
        helpUrl = QtCore.QUrl.fromLocalFile(str(self._docsPath.absolute()))
        self._widget.helpText.setSource(helpUrl)

    def discord_clicked(self):
        webbrowser.open(self._strings.discordUrl)

    def docs_clicked(self):
        webbrowser.open(self._strings.pluginDocsUrl(self._plugin.lower()))

    def nexus_clicked(self):
        webbrowser.open(self._strings.pluginNexusUrl(self._game.lower(), self._nexusId))

    def github_clicked(self):
        webbrowser.open(self._strings.githubUrl)

    def patreon_clicked(self):
        webbrowser.open(self._strings.patreonUrl)