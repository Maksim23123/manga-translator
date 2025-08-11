from PySide6.QtGui import QAction
from gui.tabs.page_editor.page_editor import PageEditor

from core.core import Core



class PageEditorController:
    def __init__(self, page_editor: PageEditor):
        self.page_editor = page_editor
        self.active_unit_index = -1
        self.core = Core()

        self._update_active_unit_combobox()

        self._connect_to_events()
        self._connect_controller()
    

    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self._reset)
        self.core.event_bus.activeUnitUpdated.connect(self._update_active_unit_combobox)
        self.core.event_bus.activeUnitChanged.connect(self._set_unit_combobox_current_index)


    def _connect_controller(self):
        self.page_editor.active_unit_comboBox.currentIndexChanged.connect(self._on_unit_combobox_current_index_changed)


    def _on_project_changed(self):
        self._update_active_unit_combobox()
    

    def _reset(self):
        self.active_unit_index = -1
        self._update_active_unit_combobox()


    def _update_active_unit_combobox(self):
        combobox = self.page_editor.active_unit_comboBox
        combobox.clear()
        self.units_list = self.core.unit_manager.get_unit_list()
        if not self.units_list:
            return
        unit_combobox_items = [unit.unit_name for unit in self.units_list]
        combobox.addItems(unit_combobox_items)

        
    def _set_unit_combobox_current_index(self):
        active_unit = self.core.unit_manager.active_unit
        
        if not self.units_list:
            return

        unit_combobox_items = [unit.unit_name for unit in self.units_list]

        if active_unit and active_unit.unit_name in unit_combobox_items:
            active_unit_index = unit_combobox_items.index(active_unit.unit_name)

            self.page_editor.active_unit_comboBox.setCurrentIndex(active_unit_index)
    

    def _on_unit_combobox_current_index_changed(self, index: int):
        if self.units_list and 0 <= index < len(self.units_list) and index != self.active_unit_index:
            self.active_unit_index = index
            new_active_unit = self.units_list[index]
            self.core.unit_manager.set_active(new_active_unit)

