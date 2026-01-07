from pathlib import Path
try:
    from ..ui.qt6.openmwplayer_texteditor import Ui_omwp_texteditor
except:
    from ..ui.qt5.openmwplayer_texteditor import Ui_omwp_texteditor
from ....common.common_qt import *

class OpenMWPlayerTextEditor(QDialog):
    """Modal text editor dialog for raw cfg file editing."""

    def __init__(self, parent: QWidget, title: str, content: str):
        super().__init__(parent)
        self._result = None
        self._setupUi(title, content)

    def _setupUi(self, title: str, content: str):
        self.ui = Ui_omwp_texteditor()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.txtEditor.setPlainText(content)
        self.ui.buttonBox.accepted.connect(self._onSave)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.setModal(True)

    def _onSave(self):
        self._result = self.ui.txtEditor.toPlainText()
        self.accept()

    def getResult(self) -> str:
        """Returns edited content, or None if cancelled."""
        return self._result

    @staticmethod
    def edit(parent: QWidget, title: str, content: str) -> str:
        """Show dialog and return edited content, or None if cancelled."""
        dialog = OpenMWPlayerTextEditor(parent, title, content)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.getResult()
        return None
