from PySide6.QtGui import QAction
from gui.tabs.page_editor.page_editor import PageEditor

from core.core import Core

from .unit_view_dock_widget_controller import UnitViewDockWidgetController



class PageEditorController:
    def __init__(self, page_editor: PageEditor):
        self.page_editor = page_editor

        self._init_subcontrollers()
    
    
    def _init_subcontrollers(self):
        self.unit_view_dock_widget_controller = UnitViewDockWidgetController(self.page_editor)
        self.unit_view_dock_widget_controller.node_selection_changed.connect(self._on_hierarchy_selection_changed)

    def _on_hierarchy_selection_changed(self, nodes):
        from core.unit_manager.hierarchy_node import HierarchyNode
        folders = [n for n in nodes if n.type == HierarchyNode.FOLDER_TYPE]
        images = [n for n in nodes if n.type == HierarchyNode.IMAGE_TYPE]
        image_paths = []
        # For folders, collect all immediate children images
        for folder in folders:
            image_paths.extend([child.image_path for child in folder.children if child.type == HierarchyNode.IMAGE_TYPE])
        # For selected images, add their paths
        image_paths.extend([img.image_path for img in images])
        # Remove duplicates while preserving order
        seen = set()
        unique_image_paths = []
        for path in image_paths:
            if path and path not in seen:
                unique_image_paths.append(path)
                seen.add(path)
        # Display images in order
        if unique_image_paths:
            self.page_editor.image_viewer_widget.set_images(unique_image_paths)

