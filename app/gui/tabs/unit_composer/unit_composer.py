from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel, QListWidgetItem
)
from .unit_composer_ui import Ui_UnitComposer
from .unit_list_item import UnitListItem
from core.core import Core

class UnitComposer(QMainWindow):
    def __init__(self, core: Core):
        super().__init__()
        self.core = core
        self._setup_ui()
        self._connect_to_events()
        
        self._update_unit_list()

    
    def _setup_ui(self):
        self.ui = Ui_UnitComposer()
        self.ui.setupUi(self)

        self.unit_listWidget = self.ui.unitListWidget
    

    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self._update_unit_list)

# Updating unit list

    def _update_unit_list(self):
        self.unit_listWidget.clear()
        unit_list = self.core.unit_manager.get_unit_list()

        for item_name in [i.unit_name for i in unit_list]:
            self._add_list_item(item_name)


    def _add_list_item(self, name):
        item_widget = UnitListItem(name)

        # Create a placeholder item
        item = QListWidgetItem(self.unit_listWidget)
        item.setSizeHint(item_widget.sizeHint())

        self.unit_listWidget.addItem(item)
        self.unit_listWidget.setItemWidget(item, item_widget)
