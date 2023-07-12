import mobase
from pathlib import Path
from .modules.moddy_settings import ModdySettings
from .modules.moddy_paths import ModdyPaths
from .moddy_dialog import ModdyDialog

try:
    from PyQt5.QtCore import QCoreApplication, qInfo
    from PyQt5.QtWidgets import QDialog
    from PyQt5 import QtWidgets, QtGui, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6.QtCore import QCoreApplication, qInfo
    from PyQt6.QtWidgets import QDialog
    from PyQt6 import QtWidgets, QtGui, QtCore
    qtSizePolicy = QtWidgets.QSizePolicy.Policy

from .checks.overwrite_files_check import OverwriteFilesCheck
from .checks.mo_in_game_check import MOInGameFolderCheck

class Moddy():
    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = ModdySettings(self.organiser)
        self.paths = ModdyPaths(self.organiser, self.settings)
        self.dialog = ModdyDialog()
        self.checklist = [
            OverwriteFilesCheck(self.organiser),
            MOInGameFolderCheck(self.organiser)
        ]

    def firstRun(self):
        dataPath = Path(self.paths.pluginDataPath())
        setupPath = dataPath.joinpath("setupcomplete.txt")
        if not setupPath.exists():
            self.notificationsWidget = self.getNotificationOptionWidget(self.dialog.dialog)
            self.dialog.setMessage("Hi, I'm Moddy, your modding companion! I can pop up and let you know when I find issues or have suggestions, alternatively you can check the notifications in Mod Organizer to find them, which would you prefer?")
            self.dialog.addOptions(self.notificationsWidget)
            self.dialog.stopBtn.setEnabled(False)
            self.dialog.closeBtn.setEnabled(False)
            self.dialog.stopBtn.setVisible(False)
            self.dialog.closeBtn.setVisible(False)
            self.dialog.show()

    def runSetupLevel(self):
        self.dialog.reset()
        self.dialog.setMessage("I can give you suggestions about your modding setup and warn you about possible problems! What kind of things would you like me to tell you about?")
        self.setupWidget = self.getSetupWidget(self.dialog.dialog)
        self.dialog.addOptions(self.setupWidget)
        self.dialog.stopBtn.setEnabled(False)
        self.dialog.closeBtn.setEnabled(False)
        self.dialog.stopBtn.setVisible(False)
        self.dialog.closeBtn.setVisible(False)
        self.dialog.show()

    def runAll(self):
        skip = self.settings.disabledchecks().split("|")
        failed = False
        failedItems = []

        messageLevel = self.settings.messagelevel()
        ix = 0
        for item in self.checklist:
            if item.identifier() not in skip and item.level() >= messageLevel:
                failed = item.check()
                if failed:
                    failedItems.append(ix)
            ix += 1

        return failedItems
    
    def checkFromIx(self, ix):
        return self.checklist[ix]

    def run(self):
        skip = self.settings.disabledchecks().split("|")
        failed = False
        failedItem = None

        messageLevel = self.settings.messagelevel()
        for item in self.checklist:
            if item.identifier() not in skip and item.level() >= messageLevel and not failed:
                failed = item.check()
                if failed:
                    failedItem = item

        if failed:
            self.dialog.reset()
            failedItem.resolve(self.dialog)

        return not failed
    
    def initialSetupLevel(self, level):
        self.organiser.setPluginSetting("Moddy", "messagelevel", level)
        dataPath = Path(self.paths.pluginDataPath())
        setupPath = dataPath.joinpath("setupcomplete.txt")
        with open(setupPath, "w", encoding="utf-8") as setupFile:
            qInfo("Moddy initial setup complete.")
            self.dialog.stopBtn.setEnabled(True)
            self.dialog.closeBtn.setEnabled(True)
            self.dialog.stopBtn.setVisible(True)
            self.dialog.closeBtn.setVisible(True)

    def initialNotificationsOnly(self, notificationsonly):
        self.organiser.setPluginSetting("Moddy", "notificationsonly", notificationsonly)

    def setupLevelNone(self):
        self.initialSetupLevel(3)
        self.dialog.reset()
        self.dialog.setMessage("Okay, I wont say a word!")

    def setupLevelCritical(self):
        self.initialSetupLevel(2)
        self.dialog.reset()
        self.dialog.setMessage("Sure thing! I'll let you know of any critical issues I notice.")

    def setupLevelIssues(self):
        self.initialSetupLevel(1)
        self.dialog.reset()
        self.dialog.setMessage("No problem, I'll keep you informed on any potential problems that might come up.")

    def setupLevelAll(self):
        self.initialSetupLevel(0)
        self.dialog.reset()
        self.dialog.setMessage("Awesome, I'll keep you updated with any thoughts I have.")
    
    def setupNotificationsOnly(self):
        self.initialNotificationsOnly(True)
        self.runSetupLevel()
    
    def setupMessagesIncluded(self):
        self.initialNotificationsOnly(False)
        self.runSetupLevel()

    def getNotificationOptionWidget(self, dialog=QDialog):
        self.notificationActions = QtWidgets.QWidget(dialog)
        self.notificationActions.setObjectName("notificationActions")
        self.notificationActions.resize(667, 104)

        self.messagesIncludedBtn = QtWidgets.QPushButton(self.notificationActions)
        self.messagesIncludedBtn.setGeometry(QtCore.QRect(10, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.messagesIncludedBtn.setFont(font)
        self.messagesIncludedBtn.setObjectName("messagesIncludedBtn")
        self.messagesIncludedBtn.clicked.connect(self.setupMessagesIncluded)
        self.messagesIncludedBtn.setText("Let me know")

        self.notificationsOnlyBtn = QtWidgets.QPushButton(self.notificationActions)
        self.notificationsOnlyBtn.setGeometry(QtCore.QRect(250, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.notificationsOnlyBtn.setFont(font)
        self.notificationsOnlyBtn.setObjectName("notificationsOnlyBtn")
        self.notificationsOnlyBtn.clicked.connect(self.setupNotificationsOnly)
        self.notificationsOnlyBtn.setText("I'll check myself")
        return self.notificationActions

    def getSetupWidget(self, dialog=QDialog):
        self.setupActions = QtWidgets.QWidget(dialog)
        self.setupActions.setObjectName("setupActions")
        self.setupActions.resize(667, 104)
        self.noneSetupBtn = QtWidgets.QPushButton(self.setupActions)
        self.noneSetupBtn.setGeometry(QtCore.QRect(10, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.noneSetupBtn.setFont(font)
        self.noneSetupBtn.setObjectName("noneSetupBtn")
        self.criticalSetupBtn = QtWidgets.QPushButton(self.setupActions)
        self.criticalSetupBtn.setGeometry(QtCore.QRect(250, 10, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.criticalSetupBtn.setFont(font)
        self.criticalSetupBtn.setObjectName("criticalSetupBtn")
        self.allSetupButton = QtWidgets.QPushButton(self.setupActions)
        self.allSetupButton.setGeometry(QtCore.QRect(250, 60, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.allSetupButton.setFont(font)
        self.allSetupButton.setObjectName("allSetupButton")
        self.issuesSetupBtn = QtWidgets.QPushButton(self.setupActions)
        self.issuesSetupBtn.setGeometry(QtCore.QRect(10, 60, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.issuesSetupBtn.setFont(font)
        self.issuesSetupBtn.setObjectName("issuesSetupBtn")
        #self.issuesSetupBtn.setAutoFillBackground(True)
        self.noneSetupBtn.setText("Don't tell me anything")
        self.criticalSetupBtn.setText("Critical issues only")
        self.issuesSetupBtn.setText("Just potential issues")
        self.allSetupButton.setText("Tell me everything")
        self.noneSetupBtn.clicked.connect(self.setupLevelNone)
        self.criticalSetupBtn.clicked.connect(self.setupLevelCritical)
        self.issuesSetupBtn.clicked.connect(self.setupLevelIssues)
        self.allSetupButton.clicked.connect(self.setupLevelAll)
        return self.setupActions



            