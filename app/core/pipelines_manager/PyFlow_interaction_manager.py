import os

from PyFlow.App import PyFlow
from PySide6.QtCore import QObject, Signal
from .pipeline_unit import PipelineUnit

from core.context import Context



class PyFlowInteractionManager:
    """
    Wrapper around PyFlow graph editor that provides a simplified API for pipeline execution.
    
    This class bridges the gap between PyFlow's visual node editor and the manga translator's
    pipeline system by exposing high-level methods for pipeline operations while hiding
    the complexity of PyFlow's internal graph structure.
    
    Key responsibilities:
    - Convert PipelineUnit data to/from PyFlow graph format
    - Execute pipeline graphs with input validation
    """

    SOFTWARE = "manga-translator"

    PIPELINES_DIR_RELATIVE_PATH = "pipelines"

    PYFLOW_GRAPH_FILE_EXTENSION = "pygraph"

    def __init__(self, context: Context):
        self._current_active_pipeline = None
        self.context = context
        self.pyflow_instance = PyFlow.instance(software=self.SOFTWARE)
    

    def set_new_active_pipeline(self, new_active_pipeline: PipelineUnit):
        if self._current_active_pipeline: 
            self.save_current_pipeline_graph()
        
        self._current_active_pipeline = new_active_pipeline

        graph_path = self._current_active_pipeline.graph_path

        if not graph_path:
            self.pyflow_instance.newFile()
            new_graph_path = self._get_unique_graph_path(self._current_active_pipeline.name)
            self.pyflow_instance.currentFileName = new_graph_path
        else:
            self.pyflow_instance.loadFromFile(graph_path)

    

    def save_current_pipeline_graph(self):
        if not os.path.exists(self.context.active_project_directory):
                raise FileNotFoundError(f"Project directory doesn't exist.")

        if self._current_active_pipeline:
            graph_path = self._current_active_pipeline.graph_path

            if not graph_path:
                graph_path = self._get_unique_graph_path(self._current_active_pipeline.name)
            
            self.pyflow_instance.currentFileName = graph_path
            self.pyflow_instance.save()
            self._current_active_pipeline.graph_path = self.pyflow_instance.currentFileName
    

    def _get_unique_graph_path(self, base_file_name: str) -> str:
        project_path = self.context.active_project_directory
        base_path = os.path.join(project_path, self.PIPELINES_DIR_RELATIVE_PATH)
        unique_path = os.path.join(base_path, f"{base_file_name}.{self.PYFLOW_GRAPH_FILE_EXTENSION}" )
        sufix_index = 1

        while os.path.exists(unique_path):
            unique_path = os.path.join(base_path, f"{base_file_name} ({sufix_index}).{self.PYFLOW_GRAPH_FILE_EXTENSION}")
            sufix_index += 1

        return unique_path

        

        

