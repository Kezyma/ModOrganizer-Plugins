from ..common.common_qt import *

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

