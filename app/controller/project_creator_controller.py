from PySide6.QtWidgets import QFileDialog, QMessageBox
from gui.windows.project_creator import ProjectCreator
from core.project_manager.project_manager import ProjectManager
import re
import os

class ProjectCreatorController:
    # Regex pattern: allows letters, numbers, underscores, dashes, and dots
    # No leading/trailing whitespace, no forbidden characters
    _VALID_NAME_PATTERN = re.compile(r"^(?!^(PRN|AUX|NUL|CON|COM\d|LPT\d)$)[a-zA-Z0-9._-]+$")


    def __init__(self, project_creator: ProjectCreator, project_manager: ProjectManager):
        self.project_creator = project_creator
        self.project_manager = project_manager

        self._connect_controller()
    

    def _connect_controller(self):
        self.project_creator.choose_location_button.clicked.connect(self.choose_location_on_click)
        self.project_creator.dialog_button_box.accepted.connect(self.dialog_button_box_accepted)
        self.project_creator.dialog_button_box.rejected.connect(self.project_creator.reject)


    def choose_location_on_click(self):
        if self.project_creator.project_path:
            base_path = self.project_creator.project_path
        else:
            base_path = self.project_manager.base_path


        new_folder_path = QFileDialog.getExistingDirectory(
            parent=self.project_creator,
            caption="Choose location",
            dir=base_path,
            options=QFileDialog.ShowDirsOnly
        )

        if new_folder_path:
            self.project_creator.set_directory(new_folder_path)
    

    def dialog_button_box_accepted(self):
        project_name = self.project_creator.project_name
        project_path = self.project_creator.project_path

        if not self.is_valid_project_name(project_name):
            self.show_warning("Invalid Project Name", "Project name cannot be empty or contain illegal characters.")
            return
        

        if not self.is_valid_project_path(project_path):
            self.show_warning("Invalid Path", "Please select a valid folder.")
            return


        self.project_manager.create_new_project(project_name, project_path)

        self.project_creator.accept()
    

    def is_valid_project_name(self, name: str) -> bool:

        name = name.strip()

        # Name must not be empty after stripping
        if not name:
            return False

        # Must match allowed pattern and avoid reserved names
        return self._VALID_NAME_PATTERN.fullmatch(name) is not None
    

    def is_valid_project_path(self, path: str) -> bool:
        if not path.strip():
            return False

        # Path must exist
        if os.path.exists(path) and os.path.isdir(path):
            return os.access(path, os.W_OK)
        
        return True

    def show_warning(self, title: str, message: str):
        QMessageBox.warning(self.project_creator, title, message)