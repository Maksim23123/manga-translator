from __future__ import annotations
import inspect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.state_persistance_manager import StatePersistanceManager



class Context:
    def __init__(self):
        self._active_project_directory = None
        self._last_active_project_directory = None
        self._state_persistance_manager = None


    @property
    def active_project_directory(self):
        return self._active_project_directory


    @active_project_directory.setter
    def active_project_directory(self, value):
        from core.project_manager.project_manager import ProjectManager
        authorized_class_name_list = [
            ProjectManager.__name__
        ]
        self.check_authorization(authorized_class_name_list)
        self._active_project_directory = value
    

    @property
    def last_active_project_directory(self):
        return self._last_active_project_directory


    @last_active_project_directory.setter
    def last_active_project_directory(self, value):
        from core.cache_manager.user_preferences import UserPreferences
        authorized_class_name_list = [
            UserPreferences.__name__
        ]
        self.check_authorization(authorized_class_name_list)
        self._last_active_project_directory = value


    @property
    def state_persistance_manager(self) -> StatePersistanceManager | None:
        return self._state_persistance_manager
    

    @state_persistance_manager.setter
    def state_persistance_manager(self, value: StatePersistanceManager):
        from core.core import Core
        from core.state_persistance_manager import StatePersistanceManager
        authorized_class_name_list = [
            Core.__name__
        ]
        self.check_authorization(authorized_class_name_list)
        if isinstance(value, StatePersistanceManager):
            self._state_persistance_manager = value
        else:
            raise TypeError(f"Expected type '{StatePersistanceManager.__name__}' got '{type(value).__name__}'")
    

    def check_authorization(self, authorized_class_name_list):
        caller = inspect.stack()[2].frame.f_locals.get("self", None)
        method_name = inspect.stack()[1].frame.f_code.co_name
        if not caller or not caller.__class__.__name__ in authorized_class_name_list:
            raise PermissionError(f"Unauthorized property modification attempt set {method_name}.")