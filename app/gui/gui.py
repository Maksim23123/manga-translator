from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QDockWidget, QTextEdit
)
from PySide6.QtCore import Qt
import sys
from .windows.project_window import ProjectWindow
from core.core import Core

class GUI():
    def __init__(self, core: Core):
        self.core = core
        self.app = QApplication(sys.argv)
        self.project_window = ProjectWindow(core)
        print("Manga Translator GUI initialized.")
        

    def show(self):
        self.project_window.show()
        sys.exit(self.app.exec())

