from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)
from .unit_list_item_ui import Ui_UnitListItem

class UnitListItem(QWidget):
    def __init__(self, unit_name: str, is_active = False):
        super().__init__()
        self._setup_ui()

        self.unit_name_label.setText(unit_name)
        self._set_activity_status(is_active)
    

    def _setup_ui(self):
        self.ui = Ui_UnitListItem()
        self.ui.setupUi(self)

        self.unit_name_label = self.ui.unitNameLabel
        self.is_active_Lable = self.ui.isActiveLabel
    

    def _set_activity_status(self, is_acitve):
        if is_acitve: self.is_active_Lable.setText("active")
        else: self.is_active_Lable.setText("")