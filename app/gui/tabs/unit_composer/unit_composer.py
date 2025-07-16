from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel, QListWidgetItem, QAbstractItemView
)
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from .unit_composer_ui import Ui_UnitComposer
from .unit_list.unit_list_item import UnitListItem
from core.core import Core
from core.unit_manager.unit import Unit
from core.unit_manager.hierarchy_node import HierarchyNode

class UnitComposer(QMainWindow):
    unit_list_updated = Signal()

    def __init__(self, core: Core):
        super().__init__()
        self.core = core
        self.unit_item_widget_list = []


        self._setup_ui()
        self._connect_to_events()
        
        self._update_unit_list()
        self._update_hierarchy_model()
        

    
    def _setup_ui(self):
        self.ui = Ui_UnitComposer()
        self.ui.setupUi(self)

        self.unit_listWidget = self.ui.unitListWidget
        self.new_unit_button = self.ui.newUnitButton
        self.import_image_button = self.ui.importFilesPushButton
        
        self.unit_hierarchy_treeView = self.ui.unitHierarchyTreeView
        self.unit_hierarchy_treeView.setEditTriggers(
                QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
            )
        self.unit_hierarchy_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.unit_hierarchy_treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.unit_hierarchy_treeView.setDragEnabled(True)
        self.unit_hierarchy_treeView.setAcceptDrops(True)
        self.unit_hierarchy_treeView.setDropIndicatorShown(True)
        self.unit_hierarchy_treeView.setDragDropMode(QAbstractItemView.InternalMove)
    

    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self._update_unit_list)
        self.core.event_bus.unitsUpdated.connect(self._update_unit_list)
        self.core.event_bus.activeUnitUpdated.connect(self._update_hierarchy_model)

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

# Update hierarchy
    def _update_hierarchy_model(self):
        active_unit = self.core.unit_manager.active_unit
        if active_unit:
            model = self._build_tree_model_from_hierarchy(active_unit.hierarchy_root)
            self.unit_hierarchy_treeView.setModel(model)

    
    def _build_tree_model_from_hierarchy(self, root_node: HierarchyNode) -> QStandardItemModel:
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name"])
        self._add_node_recursive(model.invisibleRootItem(), root_node.children)
        return model
    

    def _add_node_recursive(self, parent_item: QStandardItem, children: list[HierarchyNode]):
        for node in children:
            item = QStandardItem(node.name)
            item.setEditable(True)
            item.setData(node, Qt.UserRole)  # Attach the actual node

            # # You can set an icon based on type
            # if node.type == "folder":
            #     item.setIcon(QIcon("icons/folder.svg"))  # optional
            # else:
            #     item.setIcon(QIcon("icons/image.svg"))   # optional

            parent_item.appendRow(item)

            if node.type == "folder":
                self._add_node_recursive(item, node.children)



class HierarchyTreeModel(QStandardItemModel):
    def dropMimeData(self, data, action, row, column, parent_index):
        parent_item = self.itemFromIndex(parent_index)
        if parent_item:
            parent_node = parent_item.data(Qt.UserRole)
            if parent_node and parent_node.type != "folder":
                return False  # Only allow drop into folders
        return super().dropMimeData(data, action, row, column, parent_index)

