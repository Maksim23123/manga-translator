from PySide6.QtCore import QSettings

class UserPreferences:
    def __init__(self):
        self.settings = QSettings("MaksymSmal", "MangaTranslator")
        self.session = {}


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