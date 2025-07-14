from .user_preferences import UserPreferences

class CacheManager:
    def __init__(self):
        self.user_preferences = UserPreferences()