from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget, QTextEdit
)
from PySide6.QtCore import Qt


class SubMainWindow(QMainWindow):
    def __init__(self, index):
        super().__init__()

        # Central widget
        central_editor = QTextEdit(f"Central Area {index}")
        self.setCentralWidget(central_editor)

        # Dockable widget on the left
        dock_left = QDockWidget(f"Left Dock {index}", self)
        dock_left.setWidget(QTextEdit(f"Left Panel {index}"))
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_left)

        # Dockable widget on the right
        dock_right = QDockWidget(f"Right Dock {index}", self)
        dock_right.setWidget(QTextEdit(f"Right Panel {index}"))
        self.addDockWidget(Qt.RightDockWidgetArea, dock_right)