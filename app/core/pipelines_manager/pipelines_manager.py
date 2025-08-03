# This will do next:
#   1. Hold list of all loaded piplines(implement lazy load). Also the same object will store pipeline data project wide. 
#       This object will hold references to all piplines in the project and will be serializable. 
#       Class name for that object will be PipelineData.
#   2. Hold an instance of active pipeline.
#   3. Hold object that will managa CRUD for pipelines. Object that works with PipelineData. Class name for that object 
#       is PipelineDataModel.
#   4. Hold object that will handle pipelineData persistance between projects. It will write PipelineData to files and read 
#       it for further usage. Class name of that object is PipelineDataIO

import os
from PyFlow.App import PyFlow

from core.event_bus.event_bus import EventBus
from core.context import Context
from .pipeline_data import PipelineData
from .pipeline_data_model import PipelineDataModel
from .pipeline_data_io import PipelineDataIO
from .pipeline_unit import PipelineUnit
from .PyFlow_interaction_manager.PyFlow_interaction_manager import PyFlowInteractionManager

from core.routes import PIPELINES_DIR_RELATIVE_PATH

class PipelinesManager:
    """
    This class supposed to manage everything that is related to pipelines.
    """
    

    def __init__(self, event_bus: EventBus, context: Context):
        self.context = context
        self.event_bus = event_bus
        self.own_event_bus = event_bus.pipeline_manager_event_bus
        self._pipeline_data = None # Object that holds list of pipelines in the project.
        self._active_pipeline = None # Holds referece to currently active pipeline.

        self._pyflow_interaction_manager = PyFlowInteractionManager(self.event_bus, self.context)
        
        self.pipeline_data_io = PipelineDataIO(self.context)
        self.pipeline_data_model = PipelineDataModel(self.event_bus, context)
        
        self._connect_to_events()

        self.reload_pipeline_data()
    

    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self.reload_pipeline_data)
        self.own_event_bus.pipeline_data_model_event_bus.pipelineRemoved.connect(self._on_pipeline_deleted)
        self.event_bus.state_persistance_manager_event_bus.writeStateRequested.connect(self.save_pipeline_data)


    def _clean_up_pipeline_unrelated_graphs(self):
        project_dir = self.context.active_project_directory

        if not (project_dir and os.path.exists(project_dir)):
            return

        pipelines_dir = os.path.join(project_dir, PIPELINES_DIR_RELATIVE_PATH)

        if not (pipelines_dir and os.path.exists(pipelines_dir)):
            return

        GRAPH_FILE_EXTENSION = "pygraph"

        pipelines_dir_content = os.listdir(pipelines_dir)

        graph_files_paths = [os.path.join(pipelines_dir, graph_file_name)  for graph_file_name in pipelines_dir_content 
                             if graph_file_name.endswith(f".{GRAPH_FILE_EXTENSION}")]
        
        pipelines_names = self.pipeline_data_model.get_pipeline_names_list()
        pipelines = [self.pipeline_data_model.get_pipeline(pipeline_name) 
                     for pipeline_name in pipelines_names]

        pipeline_related_graphs_paths = [pipeline.graph_path for pipeline in pipelines if pipeline.graph_path]
        
        for graph_path_from_dir in graph_files_paths:
            if not graph_path_from_dir in pipeline_related_graphs_paths:
                os.remove(graph_path_from_dir)
    

    @property
    def pyflow_interaction_manager(self) -> PyFlowInteractionManager:
        return self._pyflow_interaction_manager


    @property
    def active_pipeline(self) -> PipelineUnit|None:
        return self._active_pipeline
    

    @property
    def pyflow_instance(self) -> PyFlow:
        return self._pyflow_interaction_manager.pyflow_instance


    def set_active_pipeline(self, pipeline_name: str) -> bool:
        if not self.pipeline_data_model.initialized:
            return False
        
        new_active_pipeline = self.pipeline_data_model.get_pipeline(pipeline_name)

        if new_active_pipeline:
            self._active_pipeline = new_active_pipeline

            self._pyflow_interaction_manager.set_new_active_pipeline(self._active_pipeline)
            self.own_event_bus.activePipelineChanged.emit(self.active_pipeline)
            return True
        
        return False

    
    def clear(self):
        """
        Clears all pipeline data and active pipline references.
        Can be used if those are getting updated, for example on
        project change, to ensure that all old data erased.
        """

        self._pipeline_data = None
        self._clear_active_pipeline()


    def reload_pipeline_data(self):
        """
        Supposed to be used on project change. It loads pipline data
        of current active project.
        """
        self.clear()

        active_project_dir = self.context.active_project_directory
        
        if active_project_dir and os.path.exists(active_project_dir):
            loaded_pipeline_data = self.pipeline_data_io.load_active_project_pipeline_data()
            self._pipeline_data = loaded_pipeline_data if loaded_pipeline_data else PipelineData()
            self.pipeline_data_model.set_pipeline_data(self._pipeline_data)
            self._clean_up_pipeline_unrelated_graphs()
    

    def save_pipeline_data(self):
        """
        Saves pipeline data to current project.
        """
        if self._pipeline_data:
            self.pipeline_data_io.write_pipeline_data_to_active_project(self._pipeline_data)


    def _on_pipeline_deleted(self, pipeline: PipelineUnit):
        if (self._active_pipeline 
                and self._active_pipeline.name == pipeline.name):
            self._clear_active_pipeline()
    

    def _clear_active_pipeline(self):
        self._active_pipeline = None
        self.own_event_bus.activePipelineChanged.emit(self._active_pipeline)