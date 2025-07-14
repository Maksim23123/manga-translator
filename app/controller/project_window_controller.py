from PySide6.QtWidgets import QFileDialog
from gui.windows.project_window import ProjectWindow
from core.core import Core
from gui.windows.project_creator import ProjectCreator
from .project_creator_controller import ProjectCreatorController

class ProjectWindowController:
    def __init__(self, core: Core, project_window: ProjectWindow):
        self.core = core
        self.project_window = project_window
        
        self._connect_controller()
    

    def _connect_controller(self):
        self.project_window.file_menu_actions["open_project"].triggered.connect(self._open_project_triggered)
        self.project_window.file_menu_actions["new_project"].triggered.connect(self._new_project_triggered)


    def _open_project_triggered(self):
        base_path = self.core.project_manager.base_path

        folder_path = QFileDialog.getExistingDirectory(
            parent=self.project_window,
            caption="Open project",
            dir=base_path,
            options=QFileDialog.ShowDirsOnly
        )

        if folder_path:
            self.core.project_manager.open_project(folder_path)
        
        #TODO: Handle cases where selected when selected folder isn't a project folder.
    

    def _new_project_triggered(self):
        base_path = self.core.project_manager.base_path

        project_creator = ProjectCreator(parent=self.project_window, default_directory=base_path)
        controller = ProjectCreatorController(project_creator, self.core.project_manager)
        project_creator.exec()

        

        