import inspect




class Context:
    def __init__(self):
        self._active_project_directory = None
        self._last_active_project_directory = None


    @property
    def active_project_directory(self):
        return self._active_project_directory


    @active_project_directory.setter
    def active_project_directory(self, value):
        from core.project_manager.project_manager import ProjectManager
        authorized_class_name_list = [
            ProjectManager.__name__
        ]
        self.check_aithorization(authorized_class_name_list)
        self._active_project_directory = value
    

    @property
    def last_active_project_directory(self):
        return self._last_active_project_directory


    @last_active_project_directory.setter
    def last_active_project_directory(self, value):
        authorized_class_name_list = [
            "UserPreferences"
        ]
        self.check_aithorization(authorized_class_name_list)
        self._last_active_project_directory = value
    

    def check_aithorization(self, authorized_class_name_list):
        caller = inspect.stack()[2].frame.f_locals.get("self", None)
        method_name = inspect.stack()[1].frame.f_code.co_name
        if not caller or not caller.__class__.__name__ in authorized_class_name_list:
            raise PermissionError(f"Unauthorized property modification attempt set {method_name}.")