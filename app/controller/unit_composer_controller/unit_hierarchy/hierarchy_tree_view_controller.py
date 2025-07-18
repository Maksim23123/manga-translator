from PySide6.QtWidgets import QTreeView, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QPoint, Qt
from core.core import Core
from .hierarchy_tree_view_model import HierarchyTreeViewModel



class HierarchyTreeViewController():
    def __init__(self, core: Core, hierarchy_treeView: QTreeView):
        self.core = core
        self.hierarchy_treeView = hierarchy_treeView

        self.model = HierarchyTreeViewModel()
        self.hierarchy_treeView.setModel(self.model)

        # Tree view configuration
        self.hierarchy_treeView.setHeaderHidden(True)
        self.hierarchy_treeView.setSelectionMode(QTreeView.SingleSelection)
        self.hierarchy_treeView.setSelectionBehavior(QTreeView.SelectRows)
        self.hierarchy_treeView.setEditTriggers(QTreeView.DoubleClicked | QTreeView.EditKeyPressed)

        self.hierarchy_treeView.setDragEnabled(True)
        self.hierarchy_treeView.setAcceptDrops(True)
        self.hierarchy_treeView.setDropIndicatorShown(True)
        self.hierarchy_treeView.setDragDropMode(QTreeView.InternalMove)
        self.hierarchy_treeView.setContextMenuPolicy(Qt.CustomContextMenu)
   
        self.hierarchy_treeView.setExpandsOnDoubleClick(True)

        self._connect_to_events()
        self._connect_controller()
    

    def _connect_to_events(self):
        self.core.event_bus.activeUnitChanged.connect(self._set_model_data)
        self.core.event_bus.activeUnitUpdated.connect(self._set_model_data)
    

    def _connect_controller(self):
        self.hierarchy_treeView.customContextMenuRequested.connect(self._open_context_menu)

    
    def _set_model_data(self):
        active_unit = self.core.unit_manager.active_unit
        if active_unit and active_unit.hierarchy_root:
            self.model.set_root_node(active_unit.hierarchy_root)
            self.hierarchy_treeView.setModel(self.model)
    

    def _open_context_menu(self, position: QPoint):
        index = self.hierarchy_treeView.indexAt(position)
        
        menu = QMenu(self.hierarchy_treeView)

        # Add folder option
        create_action = QAction("Create Folder", menu)
        create_action.triggered.connect(lambda: self.model.create_folder(index))
        menu.addAction(create_action)


        # Delete option only if node is not root
        if not self.model.is_root(index):
            delete_action = QAction("Delete", menu)
            delete_action.triggered.connect(lambda: self.model.delete_node(index))
            menu.addAction(delete_action)

        menu.exec_(self.hierarchy_treeView.viewport().mapToGlobal(position))