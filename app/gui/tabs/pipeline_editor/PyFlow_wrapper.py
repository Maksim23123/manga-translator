from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from PyFlow.App import PyFlow
from PyFlow.UI.Canvas.UICommon import SessionDescriptor

class PyFlowWrapper(QWidget):

    SOFTWARE = "manga-translator"

    def __init__(self, parent: QWidget|None=None):
        super().__init__(parent)
        

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self._setup_pyflow()

        self.main_layout.addWidget(self.pyflow_instance)

    

    def _setup_pyflow(self, parent: QWidget|None=None):
        self.pyflow_instance = PyFlow.instance(parent, self.SOFTWARE)

        self.pyflow_instance.setMenuBar(None)