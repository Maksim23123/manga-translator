from PySide6.QtWidgets import QFileDialog
from gui.windows.project_window import ProjectWindow
from core.core import Core

class ProjectWindowController:
    def __init__(self, core: Core, project_window: ProjectWindow):
        self.core = core
        self.project_window = project_window
        
        self._connect_controller()
    

    def _connect_controller(self):
        self.project_window.file_menu_actions["open_project"].triggered.connect(self._open_project_on_click)


    def _open_project_on_click(self):
        base_path = self.core.project_manager.base_path

        folder_path = QFileDialog.getExistingDirectory(
            parent=None,
            caption="Open project",
            dir=base_path,
            options=QFileDialog.ShowDirsOnly
        )

        if folder_path:
            self.core.project_manager.open_project(folder_path)
        
        # Handle cases where selected when selected folder isn't a project folder.
    

    def _new_project_on_click(self):
        base_path = self.core.project_manager.base_path

        folder_path = QFileDialog.getExistingDirectory(
            parent=None,
            caption="Open project",
            dir=base_path,
            options=QFileDialog.ShowDirsOnly
        )

        if folder_path:
            self.core.project_manager.open_project(folder_path)
        
        # Handle cases where selected when selected folder isn't a project folder.

        