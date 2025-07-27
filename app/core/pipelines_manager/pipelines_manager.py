# TODO: This will do next:
#   1. Hold list of all loaded piplines(implement lazy load). Also the same object will store pipeline data project wide. 
#       This object will hold references to all piplines in the project and will be serializable. 
#       Class name for that object will be PipelineData.
#   2. Hold an instance of active pipeline.
#   3. Hold object that will managa CRUD for pipelines. Object that works with PipelineData. Class name for that object 
#       is PipelineDataModel.
#   4. Hold object that will handle pipelineData persistance between projects. It will write PipelineData to files and read 
#       it for further usage. Class name of that object is PipelineDataIO

import inspect
import os

from core.event_bus.event_bus import EventBus
from core.context import Context
from .pipeline_data import PipelineData
from .pipeline_data_model import PipelineDataModel
from .pipeline_data_io import PipelineDataIO
from .pipeline_unit import PipelineUnit



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
        
        self.pipeline_data_io = PipelineDataIO(self.context)
        self.pipeline_data_model = PipelineDataModel(self.event_bus)
        
        self._connect_to_events()

        self.reload_pipeline_data()
    

    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self.reload_pipeline_data)


    @property
    def active_pipeline(self) -> PipelineUnit|None:
        return self._active_pipeline


    def set_active_pipeline(self, pipeline_name: str) -> bool:
        if not self.pipeline_data_model.initialized:
            return False
        
        new_active_pipeline = self.pipeline_data_model.get_pipeline(pipeline_name)

        if new_active_pipeline:
            self._active_pipeline = new_active_pipeline
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
        self._active_pipeline = None


    def reload_pipeline_data(self): # TODO: Write me
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
    

    def save_pipeline_data(self):
        """
        Saves pipeline data to current project.
        """
        if self._pipeline_data:
            self.pipeline_data_io.write_pipeline_data_to_active_project(self._pipeline_data)
