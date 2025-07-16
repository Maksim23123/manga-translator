from gui.tabs.unit_composer.unit_list.unit_list_item import UnitListItem
from core.core import Core

class UnitListItemController:
    def __init__(self, core: Core, unit_list_item_widget: UnitListItem):
        self.core = core
        self.unit_list_item_widget = unit_list_item_widget
        self._connect_controller()
        self._connect_to_events()
    

    def _connect_controller(self):
        self.unit_list_item_widget.delete_button.clicked.connect(self._delete_on_click)


    def _connect_to_events(self):
        self.core.event_bus.activeUnitChanged.connect(self._on_active_unit_chagned)


    def _delete_on_click(self):
        self.core.unit_manager.delete_unit(self.unit_list_item_widget.unit.unit_path)
    

    def _on_active_unit_chagned(self):
        new_active_unit = self.core.unit_manager.active_unit
        if new_active_unit:
            new_active_unit_path = new_active_unit.unit_path
            self.unit_list_item_widget.set_activity_status(new_active_unit_path == self.unit_list_item_widget.unit.unit_path)
                