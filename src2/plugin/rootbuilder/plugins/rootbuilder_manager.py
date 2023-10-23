import mobase
from ..core.rootbuilder_plugin import RootBuilderPlugin
try:
    from PyQt5.QtCore import QCoreApplication
    from PyQt5 import QtCore, QtWidgets
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtCore import QCoreApplication
    from PyQt6 import QtCore, QtWidgets
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy.Policy

class RootBuilderManager(RootBuilderPlugin, mobase.IPluginTool):
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self._dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self._pluginName, trstr)

    def master(self):
        return self._pluginName

    def settings(self):
        return []

    def icon(self):
        return self._icons.linkAltIcon()

    def name(self):
        return self.baseName() + " Manager Tool"

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.__tr("Opens the Root Builder Manager.")
    
    def display(self):
        self._dialog.show()
        self.bindSettings()

    def copyModeButton_clicked(self):
        """Runs when the user switches to copy mode."""
        self._rootBuilder._settings.updateSetting("copyfiles", "**")
        self._rootBuilder._settings.updateSetting("linkfiles", "")
        self._rootBuilder._settings.updateSetting("usvfsfiles", "")

    def linkModeButton_clicked(self):
        """Runs when the user switches to link mode."""
        self._rootBuilder._settings.updateSetting("linkfiles", "**")
        self._rootBuilder._settings.updateSetting("copyfiles", "")
        self._rootBuilder._settings.updateSetting("usvfsfiles", "")

    def usvfsModeButton_clicked(self):
        """Runs when the user switches to usvfs mode."""
        self._rootBuilder._settings.updateSetting("usvfsfiles", "**")
        self._rootBuilder._settings.updateSetting("linkfiles", "")
        self._rootBuilder._settings.updateSetting("copyfiles", "")

    def usvfslinkModeButton_clicked(self):
        """Runs when the user switches to usvfs + link mode."""
        self._rootBuilder._settings.updateSetting("usvfsfiles", "**")
        self._rootBuilder._settings.updateSetting("linkfiles", "**\\*.exe,**\\*.dll")
        self._rootBuilder._settings.updateSetting("copyfiles", "")
        self._rootBuilder._settings.updateSetting("usvfspriority", 30)
        self._rootBuilder._settings.updateSetting("linkpriority", 20)

    def customModeButton_clicked(self):
        """Runs when the user switches to custom mode."""

    def bindSettings(self):
        """Rebinds the window for the current settings."""
        linkFiles = self._rootBuilder._settings.linkfiles()
        copyFiles = self._rootBuilder._settings.copyfiles()
        usvfsFiles = self._rootBuilder._settings.usvfsfiles()

        linkModeOn = len(linkFiles) == 1 and linkFiles[0] == "**"
        linkModeOff = len(linkFiles) == 1 and linkFiles[0] == ""
        copyModeOn = len(copyFiles) == 1 and copyFiles[0] == "**"
        copyModeOff = len(copyFiles) == 1 and copyFiles[0] == ""
        usvfsModeOn = len(usvfsFiles) == 1 and usvfsFiles[0] == "**"
        usvfsModeOff = len(usvfsFiles) == 1 and usvfsFiles[0] == ""
        usvfsLinkModeOn = len(linkFiles) == 2 and linkFiles[0] == "**\\*.exe" and linkFiles[1] == "**\*.dll"

        linkMode = linkModeOn and copyModeOff and usvfsModeOff
        copyMode = copyModeOn and linkModeOff and usvfsModeOff
        usvfsMode = usvfsModeOn and copyModeOff and linkModeOff
        usvfsLinkMode = usvfsModeOn and usvfsLinkModeOn and copyModeOff 
        customMode = not linkMode and not copyMode and not usvfsMode and not usvfsLinkMode

        if linkMode:
            self._linkModeButton.setChecked(True)
        elif copyMode:
            self._copyModeButton.setChecked(True)
        elif usvfsMode:
            self._usvfsModeButton.setChecked(True)
        elif usvfsLinkMode:
            self._usvfsLinkModeButton.setChecked(True)
        else:
            self._customModeButton.setChecked(True)

    def getDialog(self) -> QtWidgets.QDialog:
        # Generate an empty dialog.
        dialog = self._ui.getDialog(self.displayName(), self.icon())
        dialogLayout = self._ui.getDialogLayout(dialog)

        # Generate tabs for the mode settings.
        tabWidget = QtWidgets.QTabWidget(dialog)
        dialogLayout.addWidget(tabWidget)

        # Generate simple mode select tab.
        simpleModeTab = QtWidgets.QWidget(dialog)
        simpleModeLayout = self._ui.getVWidgetLayout(simpleModeTab)
        simpleModeTab.setLayout(simpleModeLayout)
        tabWidget.addTab(simpleModeTab, self.__tr("Simple"))

        # Generate simple legacy option buttons
        self._copyModeButton = self._ui.getRadioButton(simpleModeTab, self.__tr("Copy"))
        self._linkModeButton = self._ui.getRadioButton(simpleModeTab, self.__tr("Link"))
        self._usvfsModeButton = self._ui.getRadioButton(simpleModeTab, self.__tr("USVFS"))
        self._usvfsLinkModeButton = self._ui.getRadioButton(simpleModeTab, self.__tr("USVFS + Link"))
        self._customModeButton = self._ui.getRadioButton(simpleModeTab, self.__tr("Custom"))
        simpleModeLayout.addWidget(self._copyModeButton)
        simpleModeLayout.addWidget(self._linkModeButton)
        simpleModeLayout.addWidget(self._usvfsModeButton)
        simpleModeLayout.addWidget(self._usvfsLinkModeButton)
        simpleModeLayout.addWidget(self._customModeButton)
        self._copyModeButton.clicked.connect(self.copyModeButton_clicked)
        self._linkModeButton.clicked.connect(self.linkModeButton_clicked)
        self._usvfsModeButton.clicked.connect(self.usvfsModeButton_clicked)
        self._usvfsLinkModeButton.clicked.connect(self.usvfslinkModeButton_clicked)
        self._customModeButton.clicked.connect(self.customModeButton_clicked)

        # Generate advanced mode tab select.
        advancedModeTab = QtWidgets.QWidget(dialog)
        advancedModeLayout = self._ui.getHWidgetLayout(advancedModeTab)
        advancedModeTab.setLayout(advancedModeLayout)
        tabWidget.addTab(advancedModeTab, self.__tr("Advanced"))

        # Generate columns for each file type.
        # TODO: Redo this as a splitter.
        copyFilesWidget = QtWidgets.QWidget(advancedModeTab)
        copyFilesLayout = self._ui.getVWidgetLayout(copyFilesWidget)
        copyFilesWidget.setLayout(copyFilesLayout)
        copyHeading = self._ui.getLabel(copyFilesWidget, "Copy")
        copyFilesLayout.addWidget(copyHeading)
        advancedModeLayout.addWidget(copyFilesWidget)

        linkFilesWidget = QtWidgets.QWidget(advancedModeTab)
        linkFilesLayout = self._ui.getVWidgetLayout(linkFilesWidget)
        linkFilesWidget.setLayout(linkFilesLayout)
        linkHeading = self._ui.getLabel(linkFilesWidget, "Links")
        linkFilesLayout.addWidget(linkHeading)
        advancedModeLayout.addWidget(linkFilesWidget)

        usvfsFilesWidget = QtWidgets.QWidget(advancedModeTab)
        usvfsFilesLayout = self._ui.getVWidgetLayout(usvfsFilesWidget)
        usvfsFilesWidget.setLayout(usvfsFilesLayout)
        usvfsHeading = self._ui.getLabel(usvfsFilesWidget, "USVFS")
        usvfsFilesLayout.addWidget(usvfsHeading)
        advancedModeLayout.addWidget(usvfsFilesWidget)
        return dialog
