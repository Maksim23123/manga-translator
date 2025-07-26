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
        
        serialized_pipeline_data["PIPELINES_LIST_KEY"] = serialized_pipelines_list

        return serialized_pipeline_data
        
        
    @classmethod
    def get_from_raw(cls, raw_data: dict):
        
        current_method = inspect.currentframe().f_code.co_name
        raise Exception(f"Unimplemented method called: {current_method}")
