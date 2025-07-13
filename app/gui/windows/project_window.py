from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
import sys
from ..tabs.sub_main_window import SubMainWindow


class ProjectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manga Translator - [Project]")
        self.resize(1000, 700)

        self.init_menu_bar()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        for i in range(2):  # Create 2 tabs for demonstration
            self.add_tab(i)

    
    def init_menu_bar(self):
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")
        open_project_action = QAction("Open project", self)
        new_project_action = QAction("New project", self)
        file_menu.addAction(open_project_action)
        file_menu.addAction(new_project_action)


    def add_tab(self, index):
        sub_main_window = SubMainWindow(index)

        # Wrap sub-main-window in a QWidget for tab embedding
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(sub_main_window)
        self.tabs.addTab(container, f"Tab {index}")