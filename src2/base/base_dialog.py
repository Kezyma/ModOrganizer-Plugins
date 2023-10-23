import mobase
try:
    from .ui.qt6.plugin_dialog import Ui_pluginDialog
    from PyQt6 import QtCore, QtWidgets
    from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
    from PyQt6.QtGui import QIcon, QFont
    qSizePolicy = QtWidgets.QSizePolicy.Policy
    qAlignmentFlag = QtCore.Qt.AlignmentFlag
except:
    from .ui.qt5.plugin_dialog import Ui_pluginDialog
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel
    from PyQt5.QtGui import QIcon, QFont
    qSizePolicy = QtWidgets.QSizePolicy
    qAlignmentFlag = QtCore.Qt

class BaseDialog(QDialog):
    """Base plugin dialog to be used for menu plugins."""

    def __init__(self, title:str, version:str, icon:QIcon):
        super().__init__()
        self.layout(title, version, icon)

    def layout(self, title:str, version:str, icon:QIcon):
        """Generates the base plugin layout."""
        self.pluginDialog = Ui_pluginDialog()
        self.pluginDialog.setupUi(self)
        self.pluginDialog.dialogTitleLabel.setText(title)
        self.pluginDialog.dialogVersionLabel.setText(version)
        self.setWindowIcon(icon)
        self.setWindowTitle(title)
        
    def addContent(self, widget:QWidget):
        """Adds a widget to the contents of the dialog."""
        self.pluginDialog.contentLayout.addWidget(widget)

