import mobase, webbrowser
from pathlib import Path
try:
    from ..ui.qt6.shortcutter_creator import Ui_shortcutterCreator
    from ..ui.qt6.shortcutter_menu import Ui_ShortcutterMenu
    from ..ui.qt6.shortcutter_update import Ui_updateTabWidget
except:
    from ..ui.qt5.shortcutter_creator import Ui_shortcutterCreator
    from ..ui.qt5.shortcutter_menu import Ui_ShortcutterMenu
    from ..ui.qt5.shortcutter_update import Ui_updateTabWidget

from ..core.shortcutter import Shortcutter
from .shortcutter_update import ShortcutterUpdate
from ....common.common_icons import *
from ....common.common_qt import *

class ShortcutterMenu(QtWidgets.QWidget):
    """Shortcutter create widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, shortcutter:Shortcutter, update:ShortcutterUpdate):
        super().__init__(parent)
        self._organiser = organiser
        self._shortcutter = shortcutter
        self._update = update
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_ShortcutterMenu()
        self.widget.setupUi(self)

        self.createTabWidget = Ui_shortcutterCreator()
        self.createTabWidget.setupUi(self.widget.shortcutTab)

        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)

        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self.updateTabWidget.updateFoundWidget.setVisible(False)
        self.updateTabWidget.noUpdateWidget.setVisible(False)
        self.updateTabWidget.checkUpdateButton.setIcon(REFRESH_ICON)
        self.updateTabWidget.updateFoundButton.setIcon(DOWNLOAD_ICON)
        self.updateTabWidget.updateFoundButton.clicked.connect(self.updateFound_clicked)
        self.updateTabWidget.checkUpdateButton.clicked.connect(self.checkUpdate_clicked)

        self.helpTabWidget.discordButton.setIcon(DISCORD_ICON)
        self.helpTabWidget.discordButton.clicked.connect(self.discord_clicked)
        self.helpTabWidget.docsButton.setIcon(DOCS_ICON)
        self.helpTabWidget.docsButton.clicked.connect(self.docs_clicked)
        self.helpTabWidget.githubButton.setIcon(GITHUB_ICON)
        self.helpTabWidget.githubButton.clicked.connect(self.github_clicked)
        self.helpTabWidget.nexusButton.setIcon(NEXUS_ICON)
        self.helpTabWidget.nexusButton.clicked.connect(self.nexus_clicked)
        self.helpTabWidget.patreonButton.setIcon(PATREON_ICON)
        self.helpTabWidget.patreonButton.clicked.connect(self.patreon_clicked)

        helpPath = Path(__file__).parent.parent / "data" / "shortcutter_help.html"
        helpUrl = QtCore.QUrl.fromLocalFile(str(helpPath.absolute()))
        self.helpTabWidget.helpText.setSource(helpUrl)

        self.createTabWidget.btnIconPath.clicked.connect(self.selectIcon)
        self.createTabWidget.btnCreate.clicked.connect(self.createShortcut)
        self.createTabWidget.ddlApplication.currentTextChanged.connect(self.selectChange)
        self.createTabWidget.ddlProfile.currentTextChanged.connect(self.selectChange)

    def rebind(self):
        self.createTabWidget.ddlApplication.clear()
        self.createTabWidget.ddlApplication.addItems(self._shortcutter._paths.modOrganizerApps())
        self.createTabWidget.ddlProfile.clear()
        self.createTabWidget.ddlProfile.addItems(self._shortcutter._paths.fileNames(self._shortcutter._paths.subfolders(self._shortcutter._strings.moProfilesPath, False)))
        self.createTabWidget.ddlProfile.setCurrentText(self._shortcutter._strings.moProfileName)
        self.selectChange()

    def selectChange(self):
        self.createTabWidget.txtName.setText(self.createTabWidget.ddlProfile.currentText() + " - " + self.createTabWidget.ddlApplication.currentText())
        appPaths = self._shortcutter._paths.modOrganizerAppPaths()
        if self.createTabWidget.ddlApplication.currentText() in appPaths:
            iconPath = str(appPaths[self.createTabWidget.ddlApplication.currentText()])
            self.createTabWidget.lblIconPath.setText(iconPath)
            self.updateIconDisplay()

    def selectIcon(self):
        fileDialog = QFileDialog(self)
        fileDialog.setFileMode(qFileMode.AnyFile)
        fileDialog.setNameFilter("Icons (*.ico *.exe)")
        files = []
        if fileDialog.exec():
            files = fileDialog.selectedFiles()
            if len(files) > 0:
                self.createTabWidget.lblIconPath.setText(files[0])
                self.updateIconDisplay()

    def updateIconDisplay(self):
        iconFile = QtCore.QFileInfo(self.createTabWidget.lblIconPath.text())
        ip = QFileIconProvider()
        icon = ip.icon(iconFile)
        pix = icon.pixmap(QSize(23, 23))
        self.createTabWidget.imgIcon.setPixmap(pix)

    invalidCharacters = '|<>"?*:/\\'
    def createShortcut(self):
        profile = self.createTabWidget.ddlProfile.currentText()
        app = self.createTabWidget.ddlApplication.currentText()
        label = str(self.createTabWidget.txtName.text())
        for character in self.invalidCharacters:
            label = str(label).replace(character, "")
        icon = self.createTabWidget.lblIconPath.text()
        self._shortcutter.create(label, profile, app, self._shortcutter._strings.moInstanceName, icon)


    def discord_clicked(self):
        webbrowser.open("https://discord.com/invite/kPA3RrxAYz")

    def docs_clicked(self):
        webbrowser.open("https://kezyma.github.io/?p=shortcutter")

    def nexus_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/59827")

    def github_clicked(self):
        webbrowser.open("https://github.com/Kezyma/ModOrganizer-Plugins")

    def patreon_clicked(self):
        webbrowser.open("https://www.patreon.com/KezymaOnline")

    def updateFound_clicked(self):
        webbrowser.open("https://www.nexusmods.com/skyrimspecialedition/mods/59827?tab=files")
       
    def checkUpdate_clicked(self):
        """Checks for an update"""
        newVersion = self._update.getLatestVersion()
        hasUpdate = newVersion is not None
        self.updateTabWidget.updateFoundWidget.setVisible(hasUpdate)
        self.updateTabWidget.noUpdateWidget.setVisible(not hasUpdate)