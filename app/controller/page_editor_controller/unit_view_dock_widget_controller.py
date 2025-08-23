from core.core import Core
from gui.tabs.page_editor.page_editor import PageEditor
from controller.unit_composer_controller.unit_hierarchy.hierarchy_tree_view_model import HierarchyTreeViewModel
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtCore import Signal, QObject


class UnitViewDockWidgetController(QObject):
    node_selection_changed = Signal(list)  # Emits list of selected hierarchy nodes
    
    def __init__(self, page_editor: PageEditor) -> None:
        super().__init__()
        self.core = Core()
        self.active_unit_comboBox = page_editor.active_unit_comboBox
        self.unit_hierarchy_tree_view = page_editor.unit_hierarchy_treeView
        self.unit_hierarchy_tree_view.setHeaderHidden(True)
        self.unit_hierarchy_model = HierarchyTreeViewModel(self.core, parent=self.unit_hierarchy_tree_view)
        self.unit_hierarchy_tree_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.unit_hierarchy_tree_view.setModel(self.unit_hierarchy_model)

        self._update_active_unit_combobox()
        self._set_unit_combobox_current_index()
        self._update_unit_hierarchy_tree_view()
        self._connect_to_events()
        self._connect_controller()
        self.unit_hierarchy_tree_view.selectionModel().selectionChanged.connect(self._on_selection_changed)
   
    def _on_selection_changed(self, selected, deselected):
        indexes = self.unit_hierarchy_tree_view.selectionModel().selectedIndexes()
        nodes = [self.unit_hierarchy_model.get_node(index) for index in indexes if index.isValid()]
        self.node_selection_changed.emit(nodes)

    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self._update_active_unit_combobox)
        self.core.event_bus.unitsUpdated.connect(self._update_active_unit_combobox)
        self.core.event_bus.activeUnitUpdated.connect(self._update_active_unit_combobox)
        self.core.event_bus.activeUnitChanged.connect(self._on_active_unit_changed)


    def _connect_controller(self):
        self.active_unit_comboBox.currentIndexChanged.connect(self._on_unit_combobox_current_index_changed)
    
    
    def _on_active_unit_changed(self):
        self._set_unit_combobox_current_index()
        self._update_unit_hierarchy_tree_view()
    
    
    def _update_unit_hierarchy_tree_view(self):
        if active_unit := self.core.unit_manager.active_unit:
            self.unit_hierarchy_model.set_root_node(active_unit.hierarchy_root)
            self.unit_hierarchy_tree_view.setModel(self.unit_hierarchy_model)
        
    
    def _update_active_unit_combobox(self):
        self.active_unit_comboBox
        self.active_unit_comboBox.clear()
        self.units_list = self.core.unit_manager.get_unit_list()
        if not self.units_list:
            return
        unit_combobox_items = [unit.unit_name for unit in self.units_list if unit is not None]
        self.active_unit_comboBox.addItems(unit_combobox_items)

        
    def _set_unit_combobox_current_index(self):
        active_unit = self.core.unit_manager.active_unit
        
        if not self.units_list:
            return

        unit_combobox_items = [unit.unit_name for unit in self.units_list if unit is not None]

        if active_unit and active_unit.unit_name in unit_combobox_items:
            active_unit_index = unit_combobox_items.index(active_unit.unit_name)

            self.active_unit_comboBox.setCurrentIndex(active_unit_index)
        else:
            self.active_unit_comboBox.setCurrentIndex(-1)
    

    def _on_unit_combobox_current_index_changed(self, index: int):
        if self.units_list and 0 <= index < len(self.units_list):
            self.active_unit_index = index
            new_active_unit = self.units_list[index]
            self.core.unit_manager.set_active(new_active_unit)