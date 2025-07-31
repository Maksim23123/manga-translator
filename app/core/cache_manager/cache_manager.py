import os

from .user_preferences import UserPreferences
from ..event_bus.event_bus import EventBus
from ..context import Context

class CacheManager:
    def __init__(self, event_bus: EventBus, context: Context):
        self.event_bus = event_bus
        self.context = context
        self.user_preferences = UserPreferences(self.event_bus, self.context)

        self._connect_to_events()


    def _connect_to_events(self):
        self.event_bus.state_persistance_manager_event_bus.writeStateRequested.connect(self._clear_on_project_save)

    
    def _clear_on_project_save(self):
        files_to_clean_up = self.context.files_to_clean_up_set

        for file_path in files_to_clean_up:
            if isinstance(file_path, str) and os.path.exists(file_path):
                os.remove(file_path)
            else:
                print(f"Warning - invalid file path: {file_path}")
        
        files_to_clean_up.clear()