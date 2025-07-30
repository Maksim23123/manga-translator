import inspect



class PipelineUnit:
    """Represents pipeline in manga translator code base"""
    NAME_KEY = "name"
    GRAPH_PATH_KEY = "graph_path"

    def __init__(self, name):
        self._name = name
        self._on_change_callable_list = list()
        self._graph_path = None
    

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.unit_changed()
    

    @property
    def graph_path(self) -> str:
        return self._graph_path
    

    @graph_path.setter
    def graph_path(self, value: str):
        
        if value == self._graph_path:
            return
        
        if not isinstance(value, str):
            raise TypeError(f"Expected '{str.__name__}', got '{type(value).__name__}'")
        
        self._graph_path = value
        self.unit_changed()
        pass


    def unit_changed(self):
        for callable in self._on_change_callable_list:
            callable(self)


    def add_on_change_callable(self, callable):
        if not callable in self._on_change_callable_list:
            self._on_change_callable_list.append(callable)


    def to_dict(self):
        serialized_pipeline_unit = dict()
        
        serialized_pipeline_unit[self.NAME_KEY] = self._name

        if self.graph_path:
            serialized_pipeline_unit[self.GRAPH_PATH_KEY] = self.graph_path

        return serialized_pipeline_unit 
    

    @classmethod
    def get_from_raw(cls, raw_data: dict):

        name = raw_data[PipelineUnit.NAME_KEY]

        pipeline_unit = cls(name)

        if cls.GRAPH_PATH_KEY in raw_data.keys():
            pipeline_unit.graph_path = raw_data[cls.GRAPH_PATH_KEY] 

        return pipeline_unit