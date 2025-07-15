from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel, QListWidgetItem
)
from PySide6.QtCore import QObject, Signal
from .unit_composer_ui import Ui_UnitComposer
from .unit_list.unit_list_item import UnitListItem
from core.core import Core
from core.unit_manager.unit import Unit

class UnitComposer(QMainWindow, QObject):
    unit_list_updated = Signal()

    def __init__(self, core: Core):
        super().__init__()
        self.core = core
        self.unit_item_widget_list = []


        self._setup_ui()
        self._connect_to_events()
        
        self._update_unit_list()

    
    def _setup_ui(self):
        self.ui = Ui_UnitComposer()
        self.ui.setupUi(self)

        self.unit_listWidget = self.ui.unitListWidget
        self.new_unit_button = self.ui.newUnitButton
        self.import_image_button = self.ui.importFilesPushButton
    

    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self._update_unit_list)
        self.core.event_bus.unitsUpdated.connect(self._update_unit_list)

# Updating unit list

    def _update_unit_list(self):
        self.unit_listWidget.clear()
        self.unit_item_widget_list.clear()
        unit_list = self.core.unit_manager.get_unit_list()

        for unit in unit_list:
            is_active = False
            if self.core.unit_manager.active_unit and unit.unit_name == self.core.unit_manager.active_unit.unit_name: is_active = True
            self._add_list_item(unit, is_active)
        
        self.unit_list_updated.emit()


    def _add_list_item(self, unit: Unit, is_active=False):
        item_widget = UnitListItem(unit, is_active)

        # Create a placeholder item
        item = QListWidgetItem(self.unit_listWidget)
        item.setSizeHint(item_widget.sizeHint())

        self.unit_listWidget.addItem(item)
        self.unit_listWidget.setItemWidget(item, item_widget)

        self.unit_item_widget_list.append(item_widget)
