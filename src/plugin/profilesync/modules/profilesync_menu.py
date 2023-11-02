from ....common import common_icons
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
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_profileSyncMenuWidget()
        self.widget.setupUi(self)

        self.groupsTabWidget = Ui_profileSyncGroupsTabWidget()
        self.groupsTabWidget.setupUi(self.widget.groupsTab)
        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self.helpTabWidget.discordButton.setIcon(common_icons.DISCORD_ICON)
        self.helpTabWidget.discordButton.clicked.connect(self.discord_clicked)
        self.helpTabWidget.docsButton.setIcon(common_icons.DOCS_ICON)
        self.helpTabWidget.docsButton.clicked.connect(self.docs_clicked)
        self.helpTabWidget.githubButton.setIcon(common_icons.GITHUB_ICON)
        self.helpTabWidget.githubButton.clicked.connect(self.github_clicked)
        self.helpTabWidget.nexusButton.setIcon(common_icons.NEXUS_ICON)
        self.helpTabWidget.nexusButton.clicked.connect(self.nexus_clicked)
        self.helpTabWidget.patreonButton.setIcon(common_icons.PATREON_ICON)
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