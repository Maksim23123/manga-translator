from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)
from .unit_list_item_ui import Ui_UnitListItem
from core.unit_manager.unit import Unit

class UnitListItem(QWidget):

    NONE_ITEM_MESSAGE = "[undefined]"

    def __init__(self, unit: Unit, is_active = False):
        super().__init__()
        self.unit = unit
        self._setup_ui()
        
        self._display_unit_data(is_active)

    def _setup_ui(self):
        self.ui = Ui_UnitListItem()
        self.ui.setupUi(self)

        self.unit_name_label = self.ui.unitNameLabel
        self.is_active_Lable = self.ui.isActiveLabel
        self.delete_button = self.ui.deleteUnitPushButton
    

    def set_activity_status(self, is_acitve):
        if is_acitve: self.is_active_Lable.setText("active")
        else: self.is_active_Lable.setText("")
    

    def _display_unit_data(self, active_status):
        if self.unit:
            self.unit_name_label.setText(self.unit.unit_name)
            self.set_activity_status(active_status)
        else:
            self.unit_name_label.setText(self.NONE_ITEM_MESSAGE)