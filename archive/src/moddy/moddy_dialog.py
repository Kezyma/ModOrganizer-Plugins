
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtGui import QIcon
    qSizePolicyFixed = QtWidgets.QSizePolicy.Fixed
    qIconModeNormal = QtGui.QIcon.Normal
    qIconStateOff = QtGui.QIcon.Off
    qAlignLeading = QtCore.Qt.AlignLeading
    qAlignLeft = QtCore.Qt.AlignLeft
    qAlignVCenter = QtCore.Qt.AlignVCenter
except:
    from PyQt6 import QtCore, QtGui, QtWidgets
    from PyQt6.QtGui import QIcon
    qSizePolicyFixed = QtWidgets.QSizePolicy.Policy.Fixed
    qIconModeNormal = QtGui.QIcon.Mode.Normal
    qIconStateOff = QtGui.QIcon.State.Off
    qAlignLeading = QtCore.Qt.AlignmentFlag.AlignLeading
    qAlignLeft = QtCore.Qt.AlignmentFlag.AlignLeft
    qAlignVCenter = QtCore.Qt.AlignmentFlag.AlignVCenter

from pathlib import Path

class ModdyDialog:
    def __init__(self):
        self.dialog = self.getDialog()

    def setCheckName(self, check=str):
        self.currentCheck = check

    def setMessage(self, message=str):
        self.messageTxt.setText(message)

    def show(self):
        self.dialog.show()

    def hide(self):
        self.dialog.hide()
        self.reset()

    def reset(self):
        self.clearLayout(self.actionsLayout)
        self.stopBtn.clicked.disconnect()
        self.closeBtn.clicked.disconnect()
        self.stopBtn.clicked.connect(self.hide)
        self.closeBtn.clicked.connect(self.hide)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

    def addOptions(self, optionWidget=QtWidgets.QWidget):
        self.actionsLayout.addWidget(optionWidget)

    def getDialog(self):
        imagePath = Path(__file__).parent.joinpath("images")
        ico = QIcon(str(Path(__file__).parent.joinpath("shared").joinpath("icons").joinpath("ui-clip.ico")))

        dialog = QtWidgets.QDialog()
        dialog.setObjectName("moddyDialog")
        dialog.resize(829, 209)
        dialog.setWindowIcon(ico)
        sizePolicy = QtWidgets.QSizePolicy(qSizePolicyFixed, qSizePolicyFixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setWindowOpacity(1.0)
        dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        dialog.setMaximumWidth(dialog.width())
        dialog.setMaximumHeight(dialog.height())
        dialog.setMinimumWidth(dialog.width())
        dialog.setMinimumHeight(dialog.height())
        dialog.setModal(True)
        
        self.moddyImg = QtWidgets.QLabel(dialog)
        self.moddyImg.setText("")
        self.moddyImg.setPixmap(QtGui.QPixmap(str(imagePath.joinpath("moddy.png"))))
        self.moddyImg.setScaledContents(True)
        self.moddyImg.setGeometry(QtCore.QRect(650, 10, 161, 191))
        self.moddyImg.setObjectName("moddyImg")
        self.bubbleImg = QtWidgets.QLabel(dialog)
        self.bubbleImg.setGeometry(QtCore.QRect(10, 10, 651, 111))
        self.bubbleImg.setText("")
        self.bubbleImg.setPixmap(QtGui.QPixmap(str(imagePath.joinpath("speech.png"))))
        self.bubbleImg.setScaledContents(True)
        self.bubbleImg.setObjectName("bubbleImg")
        self.stopBtn = QtWidgets.QPushButton(dialog)
        self.stopBtn.setGeometry(QtCore.QRect(610, 160, 41, 41))
        self.stopBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(str(imagePath.joinpath("stop.png"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopBtn.setIcon(icon1)
        self.stopBtn.setIconSize(QtCore.QSize(32, 32))
        self.stopBtn.setFlat(True)
        self.stopBtn.setObjectName("stopBtn")
        self.stopBtn.clicked.connect(self.hide)
        self.closeBtn = QtWidgets.QPushButton(dialog)
        self.closeBtn.setGeometry(QtCore.QRect(910, 0, 41, 41))
        self.closeBtn.setText("")
        self.closeBtn.setGeometry(QtCore.QRect(780, 0, 41, 41))
        self.closeBtn.clicked.connect(self.hide)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(imagePath.joinpath("close.png"))), qIconModeNormal, qIconStateOff)
        self.closeBtn.setIcon(icon)
        self.closeBtn.setIconSize(QtCore.QSize(32, 32))
        self.closeBtn.setFlat(True)
        self.closeBtn.setObjectName("closeBtn")
        self.messageTxt = QtWidgets.QLabel(dialog)
        self.messageTxt.setGeometry(QtCore.QRect(20, 10, 621, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.messageTxt.setFont(font)
        self.messageTxt.setAlignment(qAlignLeading|qAlignLeft|qAlignVCenter)
        self.messageTxt.setWordWrap(True)

        self.actionsWidget = QtWidgets.QWidget(dialog)
        self.actionsWidget.setGeometry(QtCore.QRect(0, 100, 611, 111))
        self.actionsWidget.setObjectName("actionsWidget")
        self.actionsLayout = QtWidgets.QVBoxLayout(self.actionsWidget)
        self.actionsLayout.setContentsMargins(0, 0, 0, 0)
        self.actionsLayout.setObjectName("actionsLayout")

        self.messageTxt.setObjectName("messageTxt")
        dialog.setWindowTitle("Moddy")
        self.closeBtn.setToolTip("Dismiss")
        self.stopBtn.setToolTip("Don\'t show this message again.")
        self.messageTxt.setText("Message about the current issue.")
        return dialog