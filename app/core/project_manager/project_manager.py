import os
import json
from datetime import datetime
from .project import Project
from ..event_bus import EventBus
from ..cache_manager.cache_manager import CacheManager
from ..context import Context 


class ProjectManager:

    DEFAULT_PROJECTS_DIR_PATH = "data\\projects"
    
    def __init__(self, event_bus: EventBus, context: Context):
        super().__init__()
        self.event_bus = event_bus
        self.context = context
        self.active_project = None
        self._init_projects_folder_path()
        self.open_last_project()
    

    def open_last_project(self):
        last_project_path = self.context.last_active_project_directory

        if last_project_path and os.path.exists(last_project_path):
            self.open_project(last_project_path)
        else:
            print("Warning:Project directory doesn't exist. Last project loading failed.")


    def _init_projects_folder_path(self):
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.base_path = os.path.join(root_path, self.DEFAULT_PROJECTS_DIR_PATH)


    def create_new_project(self, project_name, project_location=None, open_new_project=True):

        if project_location:
            project_path = os.path.join(project_location, project_name)
        else:
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
        if open_new_project: self.open_project(project_path)
        return project_path
    

    def open_project(self, project_path) -> bool:
        meta_file = os.path.join(project_path, "project.json")

        if not os.path.exists(meta_file):
            raise FileNotFoundError(f"Metadata not found at {meta_file}")
        with open(meta_file, "r", encoding="utf-8") as f:
            project_data = json.load(f)

        if project_data:
            self.active_project = Project(project_data)
            self.context.active_project_directory = project_path
            self.event_bus.activeProjectChanged.emit(project_path)
            return True
        return False