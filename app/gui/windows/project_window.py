from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
)
from PySide6.QtCore import Qt
import sys
from ..tabs.sub_main_window import SubMainWindow


class ProjectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manga Translator - [Project]")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        for i in range(2):  # Create 2 tabs for demonstration
            self.add_tab(i)

    def add_tab(self, index):
        sub_main_window = SubMainWindow(index)

        # Wrap sub-main-window in a QWidget for tab embedding
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(sub_main_window)
        self.tabs.addTab(container, f"Tab {index}")