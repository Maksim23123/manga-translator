from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QDockWidget, QTextEdit
)
from PySide6.QtCore import Qt
import sys
from .windows.project_window import ProjectWindow


def run_gui():
    app = QApplication(sys.argv)
    main_window = ProjectWindow()
    main_window.show()
    sys.exit(app.exec())