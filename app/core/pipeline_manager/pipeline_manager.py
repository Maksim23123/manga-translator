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

from core.event_bus import EventBus
from core.context import Context
from .pipeline_data import PipelineData
from .pipeline_data_model import PipelineDataModel
from .pipeline_data_io import PipelineDataIO



class PipelineManager:
    """
    This class supposed to manage everything that is related to pipelines.
    """
    def __init__(self, event_bus: EventBus, context: Context):
        self.context = context
        self.event_bus = event_bus
        self._pipeline_data = None # Object that holds list of pipelines in the project.
        self.active_pipeline = None # Holds referece to currently active pipeline.
        
        self.pipeline_data_io = PipelineDataIO(self.context)
        self.pipeline_data_model = PipelineDataModel()
        
        self._connect_to_events()

        self.reload_pipeline_data()

        # Test

        # self.test_new_pipeline_data_functionality()

        self.test_pipeline_data_loading()


    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self.reload_pipeline_data)

    
    def clear(self):
        """
        Clears all pipeline data and active pipline references.
        Can be used if those are getting updated, for example on
        project change, to ensure that all old data erased.
        """

        self._pipeline_data = None
        self.active_pipeline = None


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

        current_method = inspect.currentframe().f_code.co_name
        raise Exception(f"Unimplemented method called: {current_method}")
    

    def test_new_pipeline_data_functionality(self): # TODO: Remove this method on finishing base functionality of PipelineManager.
        self.reload_pipeline_data()

        self.pipeline_data_model.add_pipeline("New pipeline")
        test_pipeline1 = self.pipeline_data_model.add_pipeline("New pipeline")
        test_pipeline2 = self.pipeline_data_model.add_pipeline("New pipeline")
        self.pipeline_data_model.add_pipeline("New pipeline")

        try:
            self.pipeline_data_model.add_pipeline("   ")
        except:
            print("Can't add pipeline with empty name. Got error")
        

        print(self.pipeline_data_model.get_pipeline_names_list())
        
        self.pipeline_data_model.remove_pipeline("New pipeline")
        
        print(self.pipeline_data_model.get_pipeline_names_list())

        test_pipeline1.name = "New pipeline"
        test_pipeline2.name = "New pipeline"
        
        print(self.pipeline_data_model.get_pipeline_names_list())

        test_pipeline3 = self.pipeline_data_model.get_pipeline("New pipeline (3)")
        
        print(test_pipeline3.name)

        self.pipeline_data_io.write_pipeline_data_to_active_project(self._pipeline_data)
    

    def test_pipeline_data_loading(self):
        self.reload_pipeline_data()

        print(self.pipeline_data_model.get_pipeline_names_list())
