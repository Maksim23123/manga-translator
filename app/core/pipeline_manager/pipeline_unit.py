import inspect



class PipelineUnit:

    NAME_KEY = "name"

    def __init__(self, name):
        self._name = name
        self._on_change_callable_list = list()
    

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.unit_changed()

    
    def unit_changed(self):
        for callable in self._on_change_callable_list:
            callable(self)


    def add_on_change_callable(self, callable):
        if not callable in self._on_change_callable_list:
            self._on_change_callable_list.append(callable)


    def to_dict(self):
        serialized_pipeline_unit = dict()
        
        serialized_pipeline_unit[self.NAME_KEY] = self._name

        return serialized_pipeline_unit 
    

    @classmethod
    def get_from_raw(cls, raw_data: dict):
        
        current_method = inspect.currentframe().f_code.co_name
        raise Exception(f"Unimplemented method called: {current_method}")