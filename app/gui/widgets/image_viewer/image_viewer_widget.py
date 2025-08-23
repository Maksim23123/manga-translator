from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPixmap, QWheelEvent, QMouseEvent
from PySide6.QtCore import Qt

class ImageViewerWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._images = []

    def set_images(self, images):
        """
        Accepts a list of QPixmap or file paths. Clears previous images and displays new ones, stacking vertically and centering.
        """
        self._scene.clear()
        self._images = []
        y_offset = 0
        max_width = 0
        pixmaps = []
        for img in images:
            if isinstance(img, str):
                pixmap = QPixmap(img)
            elif isinstance(img, QPixmap):
                pixmap = img
            else:
                continue
            pixmaps.append(pixmap)
            max_width = max(max_width, pixmap.width())
        for pixmap in pixmaps:
            x = (max_width - pixmap.width()) // 2
            item = self._scene.addPixmap(pixmap)
            item.setPos(x, y_offset)
            self._images.append(pixmap)
            y_offset += pixmap.height()
        self.fitInView(self._scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def add_image(self, image):
        """
        Adds a single image below existing images, centered.
        """
        if isinstance(image, str):
            pixmap = QPixmap(image)
        elif isinstance(image, QPixmap):
            pixmap = image
        else:
            return
        # Find max width among all images including new one
        all_pixmaps = self._images + [pixmap]
        max_width = max(p.width() for p in all_pixmaps)
        # Calculate y offset
        y_offset = sum(p.height() for p in self._images)
        x = (max_width - pixmap.width()) // 2
        item = self._scene.addPixmap(pixmap)
        item.setPos(x, y_offset)
        self._images.append(pixmap)
        # Re-center all images
        y = 0
        for p_item, p in zip(self._scene.items()[::-1], all_pixmaps):
            x = (max_width - p.width()) // 2
            p_item.setPos(x, y)
            y += p.height()
        self.fitInView(self._scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def set_image(self, image):
        """
        Accepts a single QPixmap or file path. Clears previous images and displays the new one.
        """
        self.set_images([image])

    def wheelEvent(self, event: QWheelEvent):
        # Zoom only if Ctrl (Win/Linux) or Command (Mac) is pressed, otherwise scroll
        modifiers = event.modifiers()
        ctrl_pressed = modifiers & Qt.KeyboardModifier.ControlModifier
        cmd_pressed = modifiers & Qt.KeyboardModifier.MetaModifier
        if ctrl_pressed or cmd_pressed:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            zoom_in_factor = 1.25
            zoom_out_factor = 0.8
            factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
            self.scale(factor, factor)
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
