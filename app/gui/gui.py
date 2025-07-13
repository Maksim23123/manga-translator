from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QDockWidget, QTextEdit
)
from PySide6.QtCore import Qt
import sys
from .windows.project_window import ProjectWindow
from controller.controller import Contorller

class GUI():
    def __init__(self, controller: Contorller):
        self.controller = controller
        self.app = QApplication(sys.argv)
        self.main_window = ProjectWindow()
        print("Manga Translator GUI initialized.")
        self.show()
        

    def show(self):
        self.main_window.show()
        sys.exit(self.app.exec())

