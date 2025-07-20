from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QTreeView,
    QVBoxLayout, QWidget)
from .hierarchy_item_details_widget_ui import Ui_HierarchyItemDetailsWidget


class HierarchyItemDetailsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
    

    def _setup_ui(self):
        self.ui = Ui_HierarchyItemDetailsWidget()
        self.ui.setupUi(self)
        

