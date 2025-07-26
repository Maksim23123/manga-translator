class PipelineUnit:
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