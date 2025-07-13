import os
import json
from datetime import datetime
from .project import Project
from PySide6.QtCore import QObject, Signal

class ProjectManager(QObject):

    DEFAULT_PROJECTS_DIR_PATH = "data\\projects"

    active_project_changed = Signal()

    def __init__(self):
        super().__init__()
        self._init_projects_folder_path()
        self.active_project = None


    def _init_projects_folder_path(self):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.base_path = os.path.join(root_path, self.DEFAULT_PROJECTS_DIR_PATH)


    def create_new_project(self, project_name, open=True):

        project_path = os.path.join(self.base_path, project_name)
        
        if os.path.exists(project_path):
            raise FileExistsError(f"Project folder '{project_path}' already exists.")
        
        os.makedirs(project_path)

        metadata = {
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
        }

        meta_file = os.path.join(project_path, "project.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"Project '{project_name}' created at {project_path}")
        if open: self.open_project(project_path)
        return project_path
    

    def open_project(self, project_path) -> bool:
        meta_file = os.path.join(project_path, "project.json")

        if not os.path.exists(meta_file):
            raise FileNotFoundError(f"Metadata not found at {meta_file}")
        with open(meta_file, "r", encoding="utf-8") as f:
            project_data = json.load(f)

        if project_data:
            self.active_project = Project(project_data)
            self.active_project_changed.emit()
            return True
        return False