from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QSizePolicy, QToolButton, QWidget)

from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Core.Common import Direction

from qtpy import QtGui


class PreviewShelfTool(ShelfTool, QObject):
    """docstring for DemoShelfTool."""

    triggered = Signal()

    def __init__(self):
        super(PreviewShelfTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Preview pipeline result"

    @staticmethod
    def getIcon():
        icon = QIcon(QIcon.fromTheme(u"media-playback-start"))
        return icon

    @staticmethod
    def name():
        return "Preview"

    def do(self):
        self.triggered.emit()
