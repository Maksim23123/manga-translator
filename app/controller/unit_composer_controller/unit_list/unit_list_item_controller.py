from gui.tabs.unit_composer.unit_list.unit_list_item import UnitListItem
from core.core import Core

class UnitListItemController:
    def __init__(self, core: Core, unit_list_item: UnitListItem):
        self.core = core
        self.unit_list_item = unit_list_item
        self._connect_controller()
    

    def _connect_controller(self):
        self.unit_list_item.delete_button.clicked.connect(self._delete_on_click)


    def _delete_on_click(self):
        self.core.unit_manager.delete_unit(self.unit_list_item.unit.unit_path)