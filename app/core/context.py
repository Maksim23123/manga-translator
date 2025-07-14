import inspect

class Context:
    def __init__(self):
        self._active_project_directory = None

    @property
    def active_project_directory(self):
        return self._active_project_directory

    @active_project_directory.setter
    def active_project_directory(self, value):
        authorized_class_name_list = [
            "UserPreferences",
            "ProjectManager"
        ]
        caller = inspect.stack()[1].frame.f_locals.get("self", None)
        if not caller or not caller.__class__.__name__ in authorized_class_name_list:
            raise PermissionError("Unauthorized property modification attempt set active_project_directory.")
        self._active_project_directory = value