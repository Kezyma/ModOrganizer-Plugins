try:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtGui import QIcon
    qtHLine = QtWidgets.QFrame.HLine
    qtSunken = QtWidgets.QFrame.Sunken
    qtStaysOnTop = QtCore.Qt.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy
except:
    from PyQt6 import QtCore, QtWidgets
    from PyQt6.QtGui import QIcon
    qtHLine = QtWidgets.QFrame.Shape.HLine
    qtSunken = QtWidgets.QFrame.Shadow.Sunken
    qtStaysOnTop = QtCore.Qt.WindowType.WindowStaysOnTopHint
    qtSizePolicy = QtWidgets.QSizePolicy.Policy

class CommonUI():
    """Class for dialog helpers to speed up UI development."""

    def getDialog(self, title:str, icon:QIcon):
        """Generates an empty dialog."""
        dialog = QtWidgets.QDialog()
        dialog.resize(475, 340)
        dialog.setWindowIcon(icon)
        dialog.setWindowTitle(title)
        return dialog

    def getDialogLayout(self, dialog:QtWidgets.QDialog):
        """Generates the base layout for a dialog."""
        dialogLayout = QtWidgets.QVBoxLayout(dialog)
        dialogLayout.setContentsMargins(5, 5, 5, 5)
        dialogLayout.setSpacing(5)
        return dialogLayout
    
    def getVWidgetLayout(self, widget:QtWidgets.QWidget) -> QtWidgets.QVBoxLayout:
        """Gets a vertical widget layout."""
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        return layout
    
    def getHWidgetLayout(self, widget:QtWidgets.QWidget) -> QtWidgets.QHBoxLayout:
        """Gets a horizontal widget layout."""
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        return layout
    
    def getLabel(self, parent:QtWidgets.QWidget, text:str) -> QtWidgets.QLabel:
        """Gets the default text label."""
        label = QtWidgets.QLabel(parent)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Preferred, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
        label.setSizePolicy(sizePolicy)
        label.setWordWrap(True)
        label.setText(text)

    def getPushButton(self, parent:QtWidgets.QWidget, text:str, icon:QIcon) -> QtWidgets.QPushButton:
        """Gets the default button"""
        button = QtWidgets.QPushButton(parent)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy)
        button.setIcon(icon)
        button.setText(text)
        return button

    def getCheckbox(self, parent:QtWidgets.QWidget, text:str) -> QtWidgets.QCheckBox:
        """Gets the default checkbox"""
        check = QtWidgets.QCheckBox(parent)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(check.sizePolicy().hasHeightForWidth())
        check.setSizePolicy(sizePolicy)
        check.setMinimumSize(QtCore.QSize(75, 0))
        check.setText(text)
        return check
    
    def getRadioButton(self, parent:QtWidgets.QWidget, text:str) -> QtWidgets.QRadioButton:
        """Gets the default radio button"""
        radio = QtWidgets.QRadioButton(parent)
        sizePolicy = QtWidgets.QSizePolicy(qtSizePolicy.Fixed, qtSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(radio.sizePolicy().hasHeightForWidth())
        radio.setSizePolicy(sizePolicy)
        radio.setMinimumSize(QtCore.QSize(75, 0))
        radio.setText(text)
        return radio

        

