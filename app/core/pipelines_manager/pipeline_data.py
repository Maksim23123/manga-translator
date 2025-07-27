import inspect
from .pipeline_unit import PipelineUnit



class PipelineData:

    PIPELINES_LIST_KEY = "pipelines_list"

    def __init__(self):
        self._pipelines_list = list()
    

    @property
    def pipelines_list(self) -> list[PipelineUnit]:
        return self._pipelines_list

    
    @pipelines_list.setter
    def pipelines_list(self, value: list[PipelineUnit]):
        if not isinstance(value, list):
            raise Exception(f"Expected list, got {type(value).__name__}.")
        
        for i, item in enumerate(value):
            if not isinstance(item, PipelineUnit):
                raise TypeError(f"All list items must be {PipelineUnit.__name__} instances")
        
        self._pipelines_list = value
    

    def to_dict(self):
        serialized_pipeline_data = dict()

        serialized_pipelines_list = list()
        for pipeline in self.pipelines_list:
            serialized_pipelines_list.append(pipeline.to_dict())
        
        serialized_pipeline_data[self.PIPELINES_LIST_KEY] = serialized_pipelines_list

        return serialized_pipeline_data
        
        
    @classmethod
    def get_from_raw(cls, raw_data: dict):
        """Create instance from serialized dictionary data"""
        if not isinstance(raw_data, dict):
            raise TypeError(f"Expected dict, got {type(raw_data).__name__}")
        
        if not cls.PIPELINES_LIST_KEY in raw_data.keys():
            raise KeyError(f"Required key is missing: {cls.PIPELINES_LIST_KEY}")
        raw_pipelines_list = raw_data[PipelineData.PIPELINES_LIST_KEY]

        instance = cls()

        pipelines_list = [PipelineUnit.get_from_raw(pipeline_raw) for pipeline_raw in raw_pipelines_list]
        instance.pipelines_list = pipelines_list #Triggers validation

        return instance
