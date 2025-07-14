from .project_manager.project_manager import ProjectManager
from .cache_manager.cache_manager import CacheManager
from .event_bus import EventBus
from .context import Context
from .unit_manager.unit_manager import UnitManager

class Core:
    def __init__(self):
        self.event_bus = EventBus()
        self.context = Context()
        self.cache_manager = CacheManager(self.event_bus, self.context)
        self.project_manager = ProjectManager(self.event_bus, self.context)
        self.unit_manager = UnitManager(self.event_bus, self.context)
        print("Manga Translator core initialized.")