from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QVBoxLayout, QWidget)
from .unit_creation_dialog_ui import Ui_newUnitDialog


class UnitCreationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self._apply_ui()
        self._setup_ui()
    

    def _apply_ui(self):
        self.ui = Ui_newUnitDialog()
        self.ui.setupUi(self)

        self.unit_name_lineEdit = self.ui.unitNameLineEdit
        self.dialog_button_box = self.ui.buttonBox
    

    def _setup_ui(self):
        self.setWindowTitle("New Manga")
    

    @property
    def unit_name(self):
        if self.unit_name_lineEdit:
            return self.unit_name_lineEdit.text()
        else:
            return None