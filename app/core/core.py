from .project_manager.project_manager import ProjectManager
from .cache_manager.cache_manager import CacheManager
from .event_bus.event_bus import EventBus
from .context import Context
from .unit_manager.unit_manager import UnitManager
from .pipelines_manager.pipelines_manager import PipelinesManager
from .state_persistance_manager import StatePersistanceManager

import threading

# TODO: Make this class a proper singleton (Use method with __new__)
class Core:

    _instance = None
    _initialized = False
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if not Core._initialized:
            self.event_bus = EventBus()
            self.context = Context()
            self.state_persistance_manager = StatePersistanceManager(self.event_bus)
            self.context.state_persistance_manager = self.state_persistance_manager
            self.cache_manager = CacheManager(self.event_bus, self.context)
            self.project_manager = ProjectManager(self.event_bus, self.context)
            self.unit_manager = UnitManager(self.event_bus, self.context)
            self.pipelines_manager = PipelinesManager(self.event_bus, self.context)
            

            Core._initialized = True
            print("Manga Translator core initialized.")