import mobase, webbrowser
from pathlib import Path
try:
    from ..ui.qt6.openmwplayer_menu import Ui_OMWPMenu
    from ..ui.qt6.openmwplayer_options import Ui_omwp_optionswidget
    from ..ui.qt6.openmwplayer_groundcover import Ui_omwp_groundcoverwidget
    from ..ui.qt6.openmwplayer_settings import Ui_omwp_settingswidget
    from ..ui.qt6.openmwplayer_settingsrow import Ui_omwp_settingsrow
    from ..ui.qt6.openmwplayer_archives import Ui_omwp_archiveswidget
    from ..ui.qt6.openmwplayer_openmwcfg import Ui_omwp_cfgwidget
    from ....base.ui.qt6.update_widget import Ui_updateTabWidget
except:
    from ..ui.qt5.openmwplayer_menu import Ui_OMWPMenu
    from ..ui.qt5.openmwplayer_options import Ui_omwp_optionswidget
    from ..ui.qt5.openmwplayer_groundcover import Ui_omwp_groundcoverwidget
    from ..ui.qt5.openmwplayer_settings import Ui_omwp_settingswidget
    from ..ui.qt5.openmwplayer_settingsrow import Ui_omwp_settingsrow
    from ..ui.qt5.openmwplayer_archives import Ui_omwp_archiveswidget
    from ..ui.qt5.openmwplayer_openmwcfg import Ui_omwp_cfgwidget
    from ....base.ui.qt5.update_widget import Ui_updateTabWidget

from ..core.openmwplayer import OpenMWPlayer
from ....common.common_update import CommonUpdate
from ....common.common_help import CommonHelp
from ....common.common_icons import *
from ....common.common_qt import *

class OpenMWPlayerMenu(QtWidgets.QWidget):
    """OpenMW main widget."""

    def __init__(self, parent:QtWidgets.QWidget, organiser:mobase.IOrganizer, openmwPlayer:OpenMWPlayer, update:CommonUpdate, help:CommonHelp):
        super().__init__(parent)
        self._organiser = organiser
        self._openmwPlayer = openmwPlayer
        self._update = update
        self._help = help
        self.generateLayout()

    def generateLayout(self):
        """Generates the full layout of the widget."""
        self.widget = Ui_OMWPMenu()
        self.widget.setupUi(self)

        self.optionsWidget = Ui_omwp_optionswidget()
        self.optionsWidget.setupUi(self.widget.optionsTab)

        self.groundcoverWidget = Ui_omwp_groundcoverwidget()
        self.groundcoverWidget.setupUi(self.widget.groundcoverTab)

        self.openmwcfgWidget = Ui_omwp_cfgwidget()
        self.openmwcfgWidget.setupUi(self.widget.openmwcfgTab)

        self.archivesWidget = Ui_omwp_archiveswidget()
        self.archivesWidget.setupUi(self.widget.archivesTab)

        self.settingsWidget = Ui_omwp_settingswidget()
        self.settingsWidget.setupUi(self.widget.settingscfgTab)

        i = 0
        self.settingsTabCollection = {}
        self.settingsRowCollection = {}
        self.settingsWidget.settingsTabs.clear()
        # Create a set of tabs.
        while i < 10:
            newTabName = f"Tab {str(i)}"

            # Create the base tab widget for this tab.
            newSettingTab = QWidget()
            newSettingLayout = QtWidgets.QVBoxLayout(newSettingTab)
            newSettingLayout.setContentsMargins(0, 0, 0, 0)
            self.settingsWidget.settingsTabs.addTab(newSettingTab, QIcon(), newTabName)

            # Add the scroll area to the tab
            scrollArea = QtWidgets.QScrollArea(parent=newSettingTab)
            scrollArea.setWidgetResizable(True)
            scrollAreaWidget = QWidget()
            scrollAreaLayout = QtWidgets.QVBoxLayout(scrollAreaWidget)
            scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
            scrollArea.setWidget(scrollAreaWidget)
            newSettingLayout.addWidget(scrollArea)

            self.settingsTabCollection[newTabName] = newSettingTab
            j = 0
            newTabRows = []
            while j < 10:
                newSettingWidget = QWidget(parent=scrollAreaWidget)
                newSettingRow = Ui_omwp_settingsrow()
                newSettingRow.setupUi(newSettingWidget)
                newSettingRow.txtSetting.setText(f"Setting Number {str(j)}")
                newTabRows.append(newSettingRow)
                scrollAreaLayout.addWidget(newSettingWidget)
                j += 1
            self.settingsRowCollection[newTabName] = newTabRows
            i += 1

        self.updateTabWidget = Ui_updateTabWidget()
        self.updateTabWidget.setupUi(self.widget.updateTab)

        self.helpTabWidget = Ui_helpTabWidget()
        self.helpTabWidget.setupUi(self.widget.helpTab)

        self._update.configure(self.updateTabWidget)
        self._help.configure(self.helpTabWidget)
