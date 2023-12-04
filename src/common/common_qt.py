try:
    from ..base.ui.qt5.plugin_dialog import Ui_pluginDialog
    from ..base.ui.qt5.progress_dialog import Ui_progressDialog
    from ..base.ui.qt5.help_widget import Ui_helpTabWidget
    from PyQt5.QtCore import QCoreApplication, QStandardPaths
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QFileDialog
    from PyQt5.QtGui import QIcon, QFont
    qItemFlag = QtCore.Qt
    qSizePolicy = QtWidgets.QSizePolicy
    qAlignmentFlag = QtCore.Qt
    qCheckState = QtCore.Qt
    qDialogCode = QtWidgets.QDialog.DialogCode
    qStandardPaths = QStandardPaths
except:
    from ..base.ui.qt6.plugin_dialog import Ui_pluginDialog
    from ..base.ui.qt6.progress_dialog import Ui_progressDialog
    from ..base.ui.qt6.help_widget import Ui_helpTabWidget
    from PyQt6.QtCore import QCoreApplication, QStandardPaths
    from PyQt6 import QtCore, QtWidgets
    from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QFileDialog
    from PyQt6.QtGui import QIcon, QFont
    qSizePolicy = QtWidgets.QSizePolicy.Policy
    qAlignmentFlag = QtCore.Qt.AlignmentFlag
    qDialogCode = QtWidgets.QDialog
    qItemFlag = QtCore.Qt.ItemFlag
    qCheckState = QtCore.Qt.CheckState
    qStandardPaths = QStandardPaths.StandardLocation