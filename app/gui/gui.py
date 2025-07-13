from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QDockWidget, QTextEdit
)
from PySide6.QtCore import Qt
import sys
from .windows.project_window import ProjectWindow
from controller.controller import Contorller
from core.core import Core

class GUI():
    def __init__(self, core: Core, controller: Contorller):
        self.controller = controller
        self.core = core
        self.app = QApplication(sys.argv)
        self.main_window = ProjectWindow(core)
        print("Manga Translator GUI initialized.")
        self.show()
        

    def show(self):
        self.main_window.show()
        sys.exit(self.app.exec())

