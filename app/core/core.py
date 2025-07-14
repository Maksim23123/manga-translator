from .project_manager.project_manager import ProjectManager
from .cache_manager.cache_manager import CacheManager
from .event_bus import EventBus

class Core:
    def __init__(self):
        self.event_bus = EventBus()
        self.cache_manager = CacheManager()
        self.project_manager = ProjectManager(self.event_bus)
        print("Manga Translator core initialized.")