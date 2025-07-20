from PySide6.QtWidgets import QFileDialog
from core.core import Core
from core.unit_manager.hierarchy_node import HierarchyNode
from gui.tabs.unit_composer.unit_composer import UnitComposer
from .unit_list.new_unit_dialog_contorller import NewUnitDialogController
from gui.tabs.unit_composer.unit_list.unit_creation_dialog import UnitCreationDialog
from .unit_list.unit_list_item_controller import UnitListItemController 
from .unit_hierarchy.hierarchy_tree_view_controller import HierarchyTreeViewController
from .details_view.details_view_controller import DetailsViewController



class UnitComposerController:
    def __init__(self, core: Core, unit_composer: UnitComposer):
        self.core = core
        self.unit_composer = unit_composer
        self.unit_item_controller_list = []

        self._init_subcontrollers()

        self._connect_controller()

        self._update_unit_item_controller_list()

    
    def _init_subcontrollers(self):
        self.hierarchy_tree_view_controller = HierarchyTreeViewController(self.core, self.unit_composer.unit_hierarchy_treeView)
        self.details_view_controller = DetailsViewController(self.core, self.unit_composer.details_view_widget)
        self.unit_composer.unit_listWidget.clicked.connect(self.details_view_controller.display_active_unit_info)

    def _connect_controller(self):
        self.unit_composer.new_unit_button.clicked.connect(self._new_unit_on_click)
        self.unit_composer.unit_list_updated.connect(self._update_unit_item_controller_list)
        self.unit_composer.import_image_button.clicked.connect(self._import_image_on_click)
        self.unit_composer.unit_listWidget.itemSelectionChanged.connect(self._unit_list_on_selection_changed)
        self.unit_composer.unit_hierarchy_treeView.clicked.connect(self._on_unit_hierarchy_clicked)


    def _update_unit_item_controller_list(self):
        self.unit_item_controller_list.clear()

        for item_widget in self.unit_composer.unit_item_widget_list:
            item_contorller = UnitListItemController(self.core, item_widget)
            self.unit_item_controller_list.append(item_contorller)


    def _new_unit_on_click(self):
        unit_creation_dialog = UnitCreationDialog()
        controller = NewUnitDialogController(unit_creation_dialog, self.core.unit_manager)
        unit_creation_dialog.exec()

    
    def _import_image_on_click(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            parent=self.unit_composer,
            caption="Import Images",
            filter="Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )

        if not file_paths:
            return  # User cancelled

        for path in file_paths:
            self.core.unit_manager.import_image(path)
    

    def _unit_list_on_selection_changed(self):
        selected_items = self.unit_composer.unit_listWidget.selectedItems()
        if selected_items:
            item = selected_items[0]
            widget = self.unit_composer.unit_listWidget.itemWidget(item)
            if widget and widget.unit:
                print(f"Newly selected unit: {widget.unit.unit_name}")
                self.core.unit_manager.set_active(widget.unit)
    

    def _on_unit_hierarchy_clicked(self):
        hierarchy_tree_view = self.unit_composer.unit_hierarchy_treeView
        indexes = hierarchy_tree_view.selectedIndexes()
        if indexes:
            index = indexes[0]

            node = index.internalPointer()
            if isinstance(node, HierarchyNode):
                self.details_view_controller.display_node(node)

