from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
import sys
from ..tabs.sub_main_window import SubMainWindow
from core.core import Core

class ProjectWindow(QMainWindow):
    WINDOW_NAME_PREFIX = "Manga Translator"


    def __init__(self, core: Core):
        super().__init__()
        self.core = core

        self._init_window_settings()
        
        self._init_gui_elements()

    
    def _init_window_settings(self):
        self.core.project_manager.active_project_changed.connect(self._update_window_name)
        self._update_window_name()

        self.resize(1000, 700)
        
    
    def _update_window_name(self):
        new_window_name = self.WINDOW_NAME_PREFIX

        active_project = self.core.project_manager.active_project

        if active_project:
            new_window_name = f"{new_window_name} - {active_project.project_name}"

        self.setWindowTitle(new_window_name)

    
    def _init_gui_elements(self):
        self._init_menu_bar()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        for i in range(2):  # Create 2 tabs for demonstration
            self._add_tab(i)
    

    def _init_menu_bar(self):
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("File")
        open_project_action = QAction("Open project", self)
        new_project_action = QAction("New project", self)
        file_menu.addAction(open_project_action)
        file_menu.addAction(new_project_action)


    def _add_tab(self, index):
        sub_main_window = SubMainWindow(index)

        # Wrap sub-main-window in a QWidget for tab embedding
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(sub_main_window)
        self.tabs.addTab(container, f"Tab {index}")