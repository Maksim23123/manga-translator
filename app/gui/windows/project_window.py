from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
import sys
from ..tabs.sub_main_window import SubMainWindow
from core.core import Core
from ..tabs.unit_composer.unit_composer import UnitComposer

class ProjectWindow(QMainWindow):
    WINDOW_NAME_PREFIX = "Manga Translator"


    def __init__(self, core: Core):
        super().__init__()
        self.core = core

        self._init_window_settings()
        
        self._init_gui_elements()

    
    def _init_window_settings(self):
        self.core.event_bus.activeProjectChanged.connect(self._update_window_name)
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

        self._add_tabs()
    

    def _init_menu_bar(self):
        self.menu_bar = self.menuBar()
        
        file_menu = self.menu_bar.addMenu("File")
        
        self.file_menu_actions = {
            "open_project": QAction("Open project", self),
            "new_project": QAction("New project", self)
        }
        
        for action in self.file_menu_actions.values():
            file_menu.addAction(action)


    def _add_tabs(self):
        self.unit_composer = UnitComposer(self.core)

        # Wrap sub-main-window in a QWidget for tab embedding
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.unit_composer)
        self.tabs.addTab(container, f"Manga Composer")