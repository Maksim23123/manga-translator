import inspect
import os
import json
from core.context import Context
from .pipeline_data import PipelineData



class PipelineDataIO:

    RELATIVE_PIPELINE_DATA_PATH = "pipelines/pipelines.json"


    def __init__(self, context: Context):
        self.context = context
    

    def load_active_project_pipeline_data(self, ) -> PipelineData|None:
        """
        Reads active project folder path from context
        and loads pipeline data.
        """
        project_directory = self.context.active_project_directory
        
        if project_directory:
            pipeline_data_path = os.path.join(project_directory
                                              , self.RELATIVE_PIPELINE_DATA_PATH)
        else:
            return
        
        if os.path.exists(pipeline_data_path):
            with open(pipeline_data_path, "r", encoding="utf-8") as f:
                try:
                    raw_pipeline_data = json.load(f)
                except json.decoder.JSONDecodeError:
                    print(f"Warning: Corupted metadata located at {pipeline_data_path}")
                    return None
                
                return PipelineData.get_from_raw(raw_pipeline_data)


    def write_pipeline_data_to_active_project(self):
        current_method = inspect.currentframe().f_code.co_name
        raise Exception(f"Unimplemented method called: {current_method}")