from ....common.common_icons import CommonIcons
from ....common.common_qt import *
from ..core.profilesync import ProfileSync
import mobase, webbrowser
from pathlib import Path

try:
    from ..ui.qt6.profilesync_menu import Ui_profileSyncMenuWidget
    from ..ui.qt6.profilesync_groups import Ui_profileSyncGroupsTabWidget
except:
    from ..ui.qt5.profilesync_menu import Ui_profileSyncMenuWidget
    from ..ui.qt5.profilesync_groups import Ui_profileSyncGroupsTabWidget

class ProfileSyncMenu(QtWidgets.QWidget):
    """Profile Sync menu widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, profileSync:ProfileSync):
        super().__init__(parent)
        self._organiser = organiser
        self._profileSync = profileSync
        self._rebind = False
        self._icons = CommonIcons()
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_profileSyncMenuWidget()
        self.widget.setupUi(self)

        self.groupsTabWidget = Ui_profileSyncGroupsTabWidget()
        self.groupsTabWidget.setupUi(self.widget.groupsTab)
        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self.helpTabWidget.discordButton.setIcon(self._icons.discordIcon())
        self.helpTabWidget.discordButton.clicked.connect(self.discord_clicked)
        self.helpTabWidget.docsButton.setIcon(self._icons.docsIcon())
        self.helpTabWidget.docsButton.clicked.connect(self.docs_clicked)
        self.helpTabWidget.githubButton.setIcon(self._icons.githubIcon())
        self.helpTabWidget.githubButton.clicked.connect(self.github_clicked)
        self.helpTabWidget.nexusButton.setIcon(self._icons.nexusIcon())
        self.helpTabWidget.nexusButton.clicked.connect(self.nexus_clicked)
        self.helpTabWidget.patreonButton.setIcon(self._icons.patreonIcon())
        self.helpTabWidget.patreonButton.clicked.connect(self.patreon_clicked)

    def discord_clicked(self):
        webbrowser.open("https://discord.com/invite/kPA3RrxAYz")

    def docs_clicked(self):
        webbrowser.open("https://kezyma.github.io/?p=profilesync")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/60690")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")

    def updateFound_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/60690?tab=files")

    def createGroup_clicked(self):
        newName = self.groupsTabWidget.newGroupText.text()
        if newName != "":
            self._profileSync._groups.createSyncGroup(newName)