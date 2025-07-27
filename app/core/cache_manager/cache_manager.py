from .user_preferences import UserPreferences
from ..event_bus.event_bus import EventBus
from ..context import Context

class CacheManager:
    def __init__(self, event_bus: EventBus, context: Context):
        self.event_bus = event_bus
        self.context = context
        self.user_preferences = UserPreferences(self.event_bus, self.context)
        # Here will be other things for managing project/manga/pipline specific cache

    