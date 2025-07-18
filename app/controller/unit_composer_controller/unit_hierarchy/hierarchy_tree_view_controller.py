from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import QTreeView, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QPoint, Qt
from core.core import Core
from .hierarchy_tree_view_model import HierarchyTreeViewModel



class HierarchyTreeViewController():
    def __init__(self, core: Core, hierarchy_treeView: QTreeView):
        self.core = core
        self.hierarchy_treeView = hierarchy_treeView

        self.model = HierarchyTreeViewModel(core)
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

        self._expanded_ids = []

        self._connect_to_events()
        self._connect_controller()
    

    def _connect_to_events(self):
        self.core.event_bus.activeUnitChanged.connect(self._set_model_data)
        self.core.event_bus.activeUnitChanged.connect(self._clear_expanded_nodes_ids)
        self.core.event_bus.activeUnitUpdated.connect(self._set_model_data)
    

    def _connect_controller(self):
        self.hierarchy_treeView.customContextMenuRequested.connect(self._open_context_menu)
        self.hierarchy_treeView.expanded.connect(self._on_expanded)
        self.hierarchy_treeView.collapsed.connect(self._on_collapse)

    
    def _set_model_data(self):
        active_unit = self.core.unit_manager.active_unit
        if active_unit and active_unit.hierarchy_root:
            self.model.set_root_node(active_unit.hierarchy_root)
            self.hierarchy_treeView.setModel(self.model)
            self._restore_expanded_nodes()
    

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


    def _restore_expanded_nodes(self):
        if not hasattr(self, "_expanded_ids"):
            return

        def recurse(index: QModelIndex):
            if not index.isValid():
                return
            node = self.model.get_node(index)
            if node.id in self._expanded_ids:
                self.hierarchy_treeView.setExpanded(index, True)
            for row in range(self.model.rowCount(index)):
                child_index = self.model.index(row, 0, index)
                recurse(child_index)

        for row in range(self.model.rowCount(QModelIndex())):
            index = self.model.index(row, 0, QModelIndex())
            recurse(index)
    

    def _on_expanded(self, index: QModelIndex):
        node = self.model.get_node(index) if index.isValid() else None

        if node:
            self._expanded_ids.append(node.id)
    

    def _on_collapse(self, index: QModelIndex):
        node = self.model.get_node(index) if index.isValid() else None

        if node and node.id in self._expanded_ids:
            self._expanded_ids.remove(node.id)
    

    def _clear_expanded_nodes_ids(self):
        self._expanded_ids.clear()
