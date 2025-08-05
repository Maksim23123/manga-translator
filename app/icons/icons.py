from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

class Icons:
    FOLDER_ICON_PATH = "app/icons/folder.png"
    IMAGE_ICON_PATH = "app/icons/image.png"
    COGWHEEL_ICON_PATH = "app/icons/cogwheel.png"
    PLAY_ICON_PATH = "app/icons/play.png"
    SETTINGS_ICON_PATH = "app/icons/settings.png"

    @classmethod
    def get_colored_icon(cls, path: str, color: QColor) -> QIcon:
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        icon = QIcon(path)
        icon.paint(painter, pixmap.rect(), Qt.AlignCenter, QIcon.Normal, QIcon.On)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()

        return QIcon(pixmap)