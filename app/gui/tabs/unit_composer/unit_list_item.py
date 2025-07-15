from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)
from .unit_list_item_ui import Ui_UnitListItem

class UnitListItem(QWidget):
    def __init__(self, unit_name: str):
        super().__init__()
        self._setup_ui()

        self.unit_name_label.setText(unit_name)
    

    def _setup_ui(self):
        self.ui = Ui_UnitListItem()
        self.ui.setupUi(self)

        self.unit_name_label = self.ui.unitNameLabel