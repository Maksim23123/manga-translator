from .user_preferences import UserPreferences
from ..event_bus import EventBus

class CacheManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.user_preferences = UserPreferences(self.event_bus)
        # Here will be other things for managing project/manga/pipline specific cache

    