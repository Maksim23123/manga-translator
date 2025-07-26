import inspect
import os
import json
from core.context import Context
from .pipeline_data import PipelineData



class PipelineDataIO:

    RELATIVE_PIPELINE_DATA_DIR_PATH = "pipelines"
    PIPELINE_DATA_FILE = "pipelines.json"

    def __init__(self, context: Context):
        self.context = context
        self.pipeline_data_path = None
    

    def get_pipeline_data_path(self):
        project_directory = self.context.active_project_directory
        
        if project_directory:
            return os.path.join(project_directory
                                              , self.RELATIVE_PIPELINE_DATA_DIR_PATH
                                              , self.PIPELINE_DATA_FILE)
        else:
            return
    

    def get_pipeline_data_dir_path(self):
        project_directory = self.context.active_project_directory
        
        if project_directory:
            return os.path.join(project_directory
                                              , self.RELATIVE_PIPELINE_DATA_DIR_PATH)
        else:
            return


    def load_active_project_pipeline_data(self) -> PipelineData|None:
        """
        Reads active project folder path from context
        and loads pipeline data.
        """
        pipeline_data_path = self.get_pipeline_data_path()
        
        if os.path.exists(pipeline_data_path):
            with open(pipeline_data_path, "r", encoding="utf-8") as f:
                try:
                    raw_pipeline_data = json.load(f)
                except json.decoder.JSONDecodeError:
                    print(f"Warning: Corupted metadata located at {pipeline_data_path}")
                    return None
                
                return PipelineData.get_from_raw(raw_pipeline_data)


    def write_pipeline_data_to_active_project(self, pipeline_data: PipelineData):
        metadata = pipeline_data.to_dict()

        os.makedirs(self.get_pipeline_data_dir_path())

        meta_file = self.get_pipeline_data_path()
        if meta_file:
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)
        else:
            raise Exception("Failed")