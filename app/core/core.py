from .project_manager.project_manager import ProjectManager

class Core:
    def __init__(self):
        self.project_manager = ProjectManager()
        print("Manga Translator core initialized.")