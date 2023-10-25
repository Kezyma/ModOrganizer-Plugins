from ..curationclub_plugin import CurationClubPlugin
import mobase
try:
    from PyQt5.QtWidgets import QInputDialog, QLineEdit
    from PyQt5.QtCore import QCoreApplication, qInfo
    from PyQt5 import QtWidgets, QtCore
    qtAlign = QtCore.Qt
    qtOrientation = QtCore.Qt
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy
    qtButtonType = QtWidgets.QDialogButtonBox
except:
    from PyQt6.QtWidgets import QInputDialog, QLineEdit
    from PyQt6.QtCore import QCoreApplication, qInfo
    from PyQt6 import QtWidgets, QtCore
    qtAlign = QtCore.Qt.AlignmentFlag
    qtOrientation = QtCore.Qt.Orientation
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy.Policy
    qtButtonType = QtWidgets.QDialogButtonBox.StandardButton

class CurationClubManageTool(CurationClubPlugin, mobase.IPluginTool):
    
    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        res = super().init(organiser)
        self.dialog = self.getDialog()
        return res

    def __tr(self, trstr):
        return QCoreApplication.translate(self.pluginName, trstr)

    def icon(self):
        return self.icons.filterIcon()
        
    def description(self):
        return self.__tr("Sorts CC content.")

    def display(self):
        self.bind()
        self.dialog.show()
        
    def bindSettings(self):
        self.rootBuilderCheck.setChecked(self.cre)

    def updateSetting(self, name, value):
        self.organiser.setPluginSetting(self.pluginName, name, value)

    def updateFormat(self):
        self.updateSetting("modnameformat", str(self.formatText.text()))

    def updateRootBuilder(self):
        self.updateSetting("rootbuildersupport", self.rootBuilderCheck.isChecked())

    def run(self):
        self.curationclub.sort()
        self.dialog.close()

    def bind(self):
        self.formatText.setText(self.curationclub.settings.modNameFormat())
        self.rootBuilderCheck.setChecked(self.curationclub.settings.rootBuilderSupport())

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setObjectName("dialog")
        dialog.resize(400, 300)
        self.dialogLayout = QtWidgets.QVBoxLayout(dialog)
        self.dialogLayout.setContentsMargins(5, 5, 5, 5)
        self.dialogLayout.setSpacing(5)
        self.dialogLayout.setObjectName("dialogLayout")
        dialog.setWindowIcon(self.icon())
        dialog.setWindowTitle("Curation Club")

        self.headingWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headingWidget.sizePolicy().hasHeightForWidth())
        self.headingWidget.setSizePolicy(sizePolicy)
        self.headingWidget.setObjectName("headingWidget")
        self.headingLayout = QtWidgets.QVBoxLayout(self.headingWidget)
        self.headingLayout.setContentsMargins(0, 0, 0, 0)
        self.headingLayout.setSpacing(5)
        self.headingLayout.setObjectName("headingLayout")
        self.headingLabel = QtWidgets.QLabel(self.headingWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headingLabel.sizePolicy().hasHeightForWidth())
        self.headingLabel.setSizePolicy(sizePolicy)
        self.headingLabel.setObjectName("headingLabel")
        self.headingLabel.setText("Curation Club")
        self.headingLayout.addWidget(self.headingLabel)
        self.headingDescLabel = QtWidgets.QLabel(self.headingWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headingDescLabel.sizePolicy().hasHeightForWidth())
        self.headingDescLabel.setSizePolicy(sizePolicy)
        self.headingDescLabel.setAlignment(qtAlign.AlignLeading|qtAlign.AlignLeft|qtAlign.AlignTop)
        self.headingDescLabel.setWordWrap(True)
        self.headingDescLabel.setObjectName("formatDescLabel")
        self.headingDescLabel.setText("Click Ok to organise Creation Club content. Your game folder and enabled mods will be searched for Creation Club content and each Creation Club item will be moved to an individual mod in Mod Organizer. This may take a while and Mod Organizer can temporarily stop responding.")
        self.headingLayout.addWidget(self.headingDescLabel)
        headingSpacer = QtWidgets.QSpacerItem(20, 0, qtSizePolicy.Minimum, qtSizePolicy.Expanding)
        self.headingLayout.addItem(headingSpacer)
        self.dialogLayout.addWidget(self.headingWidget)

        self.formatWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatWidget.sizePolicy().hasHeightForWidth())
        self.formatWidget.setSizePolicy(sizePolicy)
        self.formatWidget.setObjectName("formatWidget")
        self.formatLayout = QtWidgets.QVBoxLayout(self.formatWidget)
        self.formatLayout.setContentsMargins(0, 0, 0, 0)
        self.formatLayout.setSpacing(5)
        self.formatLayout.setObjectName("formatLayout")
        self.formatLabel = QtWidgets.QLabel(self.formatWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatLabel.sizePolicy().hasHeightForWidth())
        self.formatLabel.setSizePolicy(sizePolicy)
        self.formatLabel.setObjectName("formatLabel")
        self.formatLabel.setText("Mod Format")
        self.formatLayout.addWidget(self.formatLabel)
        self.formatDescLabel = QtWidgets.QLabel(self.formatWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.formatDescLabel.sizePolicy().hasHeightForWidth())
        self.formatDescLabel.setSizePolicy(sizePolicy)
        self.formatDescLabel.setAlignment(qtAlign.AlignLeading|qtAlign.AlignLeft|qtAlign.AlignTop)
        self.formatDescLabel.setWordWrap(True)
        self.formatDescLabel.setObjectName("formatDescLabel")
        self.formatDescLabel.setText("Specify the format for Creation Club mod names. {creation} specifies the name of the creation itself.")
        self.formatLayout.addWidget(self.formatDescLabel)
        self.formatText = QtWidgets.QLineEdit(self.formatWidget)
        self.formatText.setObjectName("formatText")
        self.formatText.textChanged.connect(self.updateFormat)
        self.formatLayout.addWidget(self.formatText)
        formatSpacer = QtWidgets.QSpacerItem(20, 0, qtSizePolicy.Minimum, qtSizePolicy.Expanding)
        self.formatLayout.addItem(formatSpacer)
        self.dialogLayout.addWidget(self.formatWidget)

        self.rootBuilderWidget = QtWidgets.QWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootBuilderWidget.sizePolicy().hasHeightForWidth())
        self.rootBuilderWidget.setSizePolicy(sizePolicy)
        self.rootBuilderWidget.setObjectName("rootBuilderWidget")
        self.rootBuilderLayout = QtWidgets.QVBoxLayout(self.rootBuilderWidget)
        self.rootBuilderLayout.setContentsMargins(0, 0, 0, 0)
        self.rootBuilderLayout.setSpacing(5)
        self.rootBuilderLayout.setObjectName("rootBuilderLayout")
        self.rootBuilderCheck = QtWidgets.QCheckBox(self.rootBuilderWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Minimum, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootBuilderCheck.sizePolicy().hasHeightForWidth())
        self.rootBuilderCheck.setSizePolicy(sizePolicy)
        self.rootBuilderCheck.setObjectName("rootBuilderCheck")
        self.rootBuilderCheck.setText("Root Builder Support")
        self.rootBuilderCheck.clicked.connect(self.updateRootBuilder)
        self.rootBuilderLayout.addWidget(self.rootBuilderCheck)
        self.rootBuilderLabel = QtWidgets.QLabel(self.rootBuilderWidget)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rootBuilderLabel.sizePolicy().hasHeightForWidth())
        self.rootBuilderLabel.setSizePolicy(sizePolicy)
        self.rootBuilderLabel.setAlignment(qtAlign.AlignLeading|qtAlign.AlignLeft|qtAlign.AlignTop)
        self.rootBuilderLabel.setWordWrap(True)
        self.rootBuilderLabel.setObjectName("rootBuilderLabel")
        self.rootBuilderLabel.setText("Enables support for Root Builder. Creation Club manifest files will also be moved to Mod Organizer inside Root folders with their respective mods. Enable if you use Root Builder, disable otherwise.")
        self.rootBuilderLayout.addWidget(self.rootBuilderLabel)
        rootBuilderSpacer = QtWidgets.QSpacerItem(20, 0, qtSizePolicy.Minimum, qtSizePolicy.Expanding)
        self.rootBuilderLayout.addItem(rootBuilderSpacer)
        self.dialogLayout.addWidget(self.rootBuilderWidget)        
        
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(qtOrientation.Horizontal)
        self.buttonBox.setStandardButtons(qtButtonType.Cancel|qtButtonType.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.dialogLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.run) # type: ignore
        self.buttonBox.rejected.connect(dialog.reject) # type: ignore
        
        QtCore.QMetaObject.connectSlotsByName(dialog)
        return dialog
        
        
        