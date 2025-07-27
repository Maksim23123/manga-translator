from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from .pipelines_list_item_ui import Ui_PipelinesListItem


class PipelinesListItem(QWidget):

    ACTIVE_ITEM_MARK = "active"
    
    def __init__(self, item_name: str, is_active: bool=False, parent: QWidget|None=None):
        super().__init__(parent)
        self.is_active = is_active

        self._setup_ui()

        self.pipeline_name_label.setText(item_name)

        self.set_active(is_active)


    def _setup_ui(self):
        self.ui = Ui_PipelinesListItem()
        self.ui.setupUi(self)

        self.pipeline_name_label = self.ui.pipeline_name_label
        self.pipeline_status_label = self.ui.pipeline_status_label
    

    def set_active(self, is_active: bool=False):
        status_label_text = self.ACTIVE_ITEM_MARK if is_active else ""
        self.pipeline_status_label.setText(status_label_text)