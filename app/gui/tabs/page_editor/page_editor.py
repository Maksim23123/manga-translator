from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel, QListWidgetItem, QAbstractItemView
)
from .page_editor_ui import Ui_PageEditor



class PageEditor(QMainWindow):
    def __init__(self, parent: QWidget|None = None):
        super().__init__(parent)
        self._apply_ui()
        self._setup_ui()

    def _apply_ui(self):
        self.ui = Ui_PageEditor()
        self.ui.setupUi(self)
        self.active_unit_comboBox = self.ui.active_unit_comboBox
        self.unit_hierarchy_treeView = self.ui.treeView

    def _setup_ui(self):
        from gui.widgets.image_viewer.image_viewer_widget import ImageViewerWidget
        self.image_viewer_widget = ImageViewerWidget(self)
        self.ui.central_widget_verticalLayout.addWidget(self.image_viewer_widget)