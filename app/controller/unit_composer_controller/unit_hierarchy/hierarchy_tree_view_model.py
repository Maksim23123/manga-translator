from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt, QMimeData, QByteArray, QDataStream, QIODevice
from core.unit_manager.hierarchy_node import HierarchyNode
from core.core import Core

# TODO: build node path system so search will be more efficient
class HierarchyTreeViewModel(QAbstractItemModel):
    def __init__(self, core: Core, root_node: HierarchyNode = HierarchyNode("root", HierarchyNode.FOLDER_TYPE), parent=None):
        super().__init__(parent)
        self.core = core
        self.root_node = root_node
        
# Base class implementation

    def index(self, row, column, parent: QModelIndex):
        parent_node = self.get_node(parent)
        if 0 <= row < len(parent_node.children):
            child_node = parent_node.children[row]
            return self.createIndex(row, column, child_node)
        return QModelIndex()
    

    def get_node(self, index: QModelIndex):
        return index.internalPointer() if index.isValid() else self.root_node
    

    def parent(self, index: QModelIndex) -> QModelIndex:
        child_node = index.internalPointer()

        parent_node = self.find_parent(self.root_node, child_node)
        
        if parent_node is None:
            return QModelIndex()
        
        grandparent_node = self.find_parent(self.root_node, parent_node)
        row = grandparent_node.children.index(parent_node) if grandparent_node else 0

        return self.createIndex(row, 0, parent_node)


    def find_parent(self, current: HierarchyNode, target: HierarchyNode):
        for child in current.children:
            if child == target:
                return current
            else:
                found = self.find_parent(child, target)
                if found:
                    return found
        return None
    

    def rowCount(self, parent: QModelIndex) -> int:
        parent_node = self.get_node(parent)
        return len(parent_node.children) if parent_node.type == HierarchyNode.FOLDER_TYPE else 0
    

    def columnCount(self, parent: QModelIndex) -> int:
        return 1
    
    
    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        node = self.get_node(index)

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if index.column() == 0:
                return node.name

        return None
    

    def flags(self, index):
        node = self.get_node(index)
        
        base_flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

        if node and node.type == HierarchyNode.FOLDER_TYPE:
            return (base_flags
                    | Qt.ItemFlag.ItemIsDragEnabled
                    | Qt.ItemFlag.ItemIsDropEnabled)  
        else:
            return base_flags | Qt.ItemFlag.ItemIsDragEnabled
    

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        
        node = self.get_node(index)
        if role == Qt.EditRole:
            node.name = str(value)
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
            self.core.event_bus.activeUnitUpdated.emit()
            return True
        
        return False


    def supportedDropActions(self):
        return Qt.DropAction.MoveAction | Qt.DropAction.CopyAction


    def mimeTypes(self):
        return ['application/x-unithierarchytreeviewmodel']


    def mimeData(self, indexes: list[QModelIndex]):
        mime_data = QMimeData()
        encoded = QByteArray()

        stream = QDataStream(encoded, QIODevice.OpenModeFlag.WriteOnly)

        for index in indexes:
            if index.isValid():
                node = self.get_node(index)
                stream.writeQString(node.id)
                break
        
        mime_data.setData(self.mimeTypes()[0], encoded)
        return mime_data
    

    def dropMimeData(self, data: QMimeData, action: Qt.DropAction, row, column, parent: QModelIndex):
        # Get draged_node
        encoded_data = data.retrieveData(self.mimeTypes()[0], QByteArray)

        stream = QDataStream(encoded_data, QIODevice.OpenModeFlag.ReadOnly)

        draged_node_id = stream.readQString()

        draged_node = self.get_node_by_id(self.root_node, draged_node_id)
        # Perform actions with dragged node
        if isinstance(draged_node, HierarchyNode):
            old_parent_node = self.find_parent(self.root_node, draged_node)
            
            draged_node_old_row = old_parent_node.children.index(draged_node)
            draged_node_index = self.createIndex(draged_node_old_row, 0, draged_node)
            old_parent_node_index = self.parent(draged_node_index)

            if old_parent_node_index.isValid():
                new_parent_node = self.get_node(parent)

                new_row_index = row if not row < 0 else len(new_parent_node.children) - 1

                if parent.isValid():
                    self.beginMoveRows(old_parent_node_index, draged_node_old_row, draged_node_old_row, parent, new_row_index)
                else:
                    self.beginResetModel()

                if old_parent_node == new_parent_node:
                    if row == draged_node_old_row:
                        return True
                    elif (row > draged_node_old_row and not action == Qt.DropAction.CopyAction):
                        row -= 1

                if action == Qt.DropAction.MoveAction:
                    old_parent_node.children.remove(draged_node)
                
                if 0 <= row < len(new_parent_node.children):
                    new_parent_node.children.insert(row, draged_node)
                else:
                    new_parent_node.children.append(draged_node)

                if parent.isValid():
                    self.endMoveRows()
                else:
                    self.endResetModel()
                
                self.core.event_bus.activeUnitUpdated.emit()

                return True
        return False


    def get_node_by_id(self, current: HierarchyNode, target_id):
        if current.id == target_id:
            return current
        else:
            for child in current.children:
                if child.type == HierarchyNode.FOLDER_TYPE:
                    found = self.get_node_by_id(child, target_id)
                    if found:
                        return found
                elif child.id == target_id:
                    return child
        
# External access

    def set_root_node(self, new_root_node: HierarchyNode):
        self.beginResetModel()
        self.root_node = new_root_node
        self.endResetModel()


    def is_root(self, index: QModelIndex) -> bool:
        node = self.get_node(index) if index.isValid() else self.root_node
        return node == self.root_node


    def create_folder(self, index: QModelIndex):
        self.beginResetModel()
        parent_node = self.get_node(index) if index.isValid() else self.root_node

        if parent_node:
            parent_node.add_folder("New folder")

        
        self.endResetModel()
    

    def delete_node(self, index: QModelIndex):
        self.beginResetModel()
        node = self.get_node(index) if index.isValid() else None
        parent_node = self.find_parent(self.root_node, node)

        if node and parent_node:
            parent_node.children.remove(node)
        self.endResetModel()
    

    def update_model(self):
        self.beginResetModel()
        self.endResetModel()