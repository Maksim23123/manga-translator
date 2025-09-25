from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel, QListWidgetItem, QAbstractItemView
)
from .page_editor_ui import Ui_PageEditor



class PageEditor(QMainWindow):
    def set_pipeline_choices(self, choices):
        self.ui.pipeline_comboBox.clear()
        self.ui.pipeline_comboBox.addItems(choices)
    def set_pipeline_value(self, value):
        # Set pipeline value in comboBox, blank if not found
        idx = self.ui.pipeline_comboBox.findText(value)
        if value == '':
            self.ui.pipeline_comboBox.setCurrentIndex(-1)
        elif idx != -1:
            self.ui.pipeline_comboBox.setCurrentIndex(idx)
        else:
            self.ui.pipeline_comboBox.setCurrentIndex(-1)

    def get_pipeline_value(self):
        return self.ui.pipeline_comboBox.currentText()

    def connect_pipeline_changed(self, slot):
        self.ui.pipeline_comboBox.currentTextChanged.connect(slot)
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self._apply_ui()
        self._setup_ui()

    def _apply_ui(self):
        self.ui = Ui_PageEditor()
        self.ui.setupUi(self)
        self.active_unit_comboBox = self.ui.active_unit_comboBox
        self.unit_hierarchy_treeView = self.ui.treeView
        self.item_settings_dock_widget = self.ui.item_settings_dockWidget

    def _setup_ui(self):
        from gui.widgets.image_viewer.image_viewer_widget import ImageViewerWidget
        self.image_viewer_widget = ImageViewerWidget(self)
        self.ui.central_widget_verticalLayout.addWidget(self.image_viewer_widget)