import re
from PySide6.QtWidgets import QMessageBox, QTreeView
from PySide6.QtGui import QPixmap
from core.core import Core
from core.unit_manager.hierarchy_node import HierarchyNode
from gui.tabs.unit_composer.details_view.details_view import DetailsView
from ..unit_list.new_unit_dialog_contorller import NewUnitDialogController



class DetailsViewController:

    _VALID_NAME_PATTERN = re.compile(r"^(?!^(PRN|AUX|NUL|CON|COM\d|LPT\d)$)[a-zA-Z0-9._-]+$")

    def __init__(self, core: Core, detailsView: DetailsView):
        self.core = core
        self.detailsView = detailsView
        self.current_node = None
        self.unit_details_widget = self.detailsView.unit_details_widget
        self.hierarchy_item_details_widget = self.detailsView.hierarchy_item_details_widget
        
        self._connect_to_events()
        self._connect_controller()


    def _connect_controller(self):
        self.unit_details_widget.save_changes_pushButton.clicked.connect(self.apply_changes_to_unit)
        self.unit_details_widget.discard_changes_pushButton.clicked.connect(self.display_active_unit_info)


    def _connect_to_events(self):
        self.core.event_bus.activeUnitChanged.connect(self.display_active_unit_info)
        self.core.event_bus.activeUnitUpdated.connect(self.display_current_node)
        
# Unit Widget related

    def display_active_unit_info(self):
        active_unit = self.core.unit_manager.active_unit
        if active_unit:
            self.unit_details_widget.unit_name_lineEdit.setText(active_unit.unit_name)
            self.unit_details_widget.unit_path_lineEdit.setText(active_unit.unit_path)
            self.detailsView.switch_display_mode(DetailsView.UNIT_DISPLAY_MODE)
        else:
            self.detailsView.switch_display_mode(DetailsView.NONE_SELECTED_DISPLAY_MODE)
    

    def apply_changes_to_unit(self):
        active_unit = self.core.unit_manager.active_unit
        unit_manager = self.core.unit_manager
        if active_unit:
            new_unit_name = self.unit_details_widget.unit_name_lineEdit.text()
            if not NewUnitDialogController.is_valid_unit_name(new_unit_name):
                QMessageBox.warning(self.unit_details_widget, "Invalid Manga Name", "Manga name cannot be empty or contain illegal characters.")
                return
            unit_manager.set_unit_name(new_unit_name)


# Hierarchy item related

    def display_current_node(self):
        self.display_node(self.current_node)


    def display_node(self, node: HierarchyNode):
        if node:
            self.current_node = node
            
            self.hierarchy_item_details_widget.item_name_lineEdit.setText(node.name) 
            self.hierarchy_item_details_widget.item_type_lineEdit.setText(node.type)

            self.detailsView.switch_display_mode(DetailsView.HIERARCHY_ITEM_DISPLAY_MODE)
            if node.type == HierarchyNode.FOLDER_TYPE:
                self._display_folder(node)
            elif node.type == HierarchyNode.IMAGE_TYPE:
                self._display_image(node)


    def _display_folder(self, node: HierarchyNode):
        self.hierarchy_item_details_widget.image_preview_label.hide()
        self.hierarchy_item_details_widget.image_path_widget.hide()

        self.hierarchy_item_details_widget.children_number_widget.show()
        
        if node:
            self.hierarchy_item_details_widget.children_number_lineEdit.setText(str(len(node.children)))
    

    def _display_image(self, node: HierarchyNode):
        self.hierarchy_item_details_widget.children_number_widget.hide()

        self.hierarchy_item_details_widget.image_preview_label.show()
        self.hierarchy_item_details_widget.image_path_widget.show()

        if node:
            self.hierarchy_item_details_widget.image_path_lineEdit.setText(node.image_path)

            pixmap = QPixmap(node.image_path)  # Use any valid image path
            image_width = pixmap.width()
            image_height = pixmap.height()

            image_width_height_ratio = image_width / image_height

            new_preview_label_height = int(self.detailsView.width() * 0.4)

            new_preview_label_width = int(new_preview_label_height * image_width_height_ratio) 

            self.hierarchy_item_details_widget.image_preview_label.setFixedSize(new_preview_label_width
                                                                                , new_preview_label_height)

            self.hierarchy_item_details_widget.image_preview_label.setPixmap(pixmap)
            self.hierarchy_item_details_widget.image_preview_label.setScaledContents(True)  # Scale the image to fit label size