from PySide6.QtCore import QSettings
from ..event_bus import EventBus
from ..context import Context

class UserPreferences:
    def __init__(self, event_bus: EventBus, context: Context):
        self.event_bus = event_bus
        self.context = context
        self.settings = QSettings("MaksymSmal", "MangaTranslator")
        self.session = {}
        self._connect_to_events()
        self._perform_initial_load()


    def get_preference(self, key, default=None):
        return self.settings.value(key, default)


    def set_preference(self, key, value):
        self.settings.setValue(key, value)


    def remember_last_project(self, path):
        self.set_preference("recent/last_project", path)


    def get_last_project(self):
        return self.get_preference("recent/last_project", "")


    # Runtime-only cache
    def set_temp(self, key, value):
        self.session[key] = value


    def get_temp(self, key, default=None):
        return self.session.get(key, default)


    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self.remember_last_project)
    

    def _perform_initial_load(self):
        self.context.active_project_directory = self.get_last_project()