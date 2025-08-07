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
from gui.tabs.pipeline_editor.PyFlow_wrapper import PyFlowWrapper
from ..tabs.page_editor.page_editor import PageEditor


class ProjectWindow(QMainWindow):
    WINDOW_NAME_PREFIX = "Manga Translator"
    PROJECT_STATUS_WINDOW_NAME_SUFIX = "*"


    def __init__(self, core: Core):
        super().__init__()
        self.core = core

        self._init_window_settings()
        
        self._connect_to_events()
        self._init_gui_elements()
    

    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self._update_window_name)
        self.core.event_bus.state_persistance_manager_event_bus.projectDataStateChanged.connect(self._update_window_name)

    
    def _init_window_settings(self):
        self._update_window_name()

        self.resize(1000, 700)
        
    
    def _update_window_name(self):
        new_window_name = self.WINDOW_NAME_PREFIX

        active_project = self.core.project_manager.active_project

        project_changed = self.core.state_persistance_manager.data_modified

        if active_project:
            new_window_name = f"{new_window_name} - {active_project.project_name} {
                self.PROJECT_STATUS_WINDOW_NAME_SUFIX if project_changed else ""
            }"

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
            "new_project": QAction("New project", self),
            "save_project": QAction("Save", self)
        }
        
        for action in self.file_menu_actions.values():
            file_menu.addAction(action)


    def _add_tabs(self):

        self.pipline_editor = PyFlowWrapper()
        self.tabs.addTab(self.pipline_editor, f"Pipeline Editor")
        
        self.unit_composer = UnitComposer(self.core)
        unit_composer_container = QWidget()
        unit_composer_layout = QVBoxLayout(unit_composer_container)
        unit_composer_layout.setContentsMargins(0, 0, 0, 0)
        unit_composer_layout.addWidget(self.unit_composer)
        self.tabs.addTab(unit_composer_container, f"Manga Composer")

        self.page_editor = PageEditor()
        self.tabs.addTab(self.page_editor, f"Page Editor")