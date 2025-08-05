import os

from PyFlow.Core.NodeBase import NodeBase
from PyFlow.App import PyFlow
from ..pipeline_unit import PipelineUnit
from .pipeline_executor import PipelineExecutor

from core.context import Context
from core.event_bus.event_bus import EventBus

from core.routes import PIPELINES_DIR_RELATIVE_PATH



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

    PYFLOW_GRAPH_FILE_EXTENSION = "pygraph"

    def __init__(self, event_bus: EventBus, context: Context):
        self._current_active_pipeline = None
        self._preview_image_path = None
        self.context = context
        self.event_bus = event_bus
        self.own_event_bus = self.event_bus.pipeline_manager_event_bus.pyflow_iteraction_manager_event_bus
        self.pyflow_instance = PyFlow.instance(software=self.SOFTWARE)
        self.executor = PipelineExecutor(self.pyflow_instance.graphManager.get())

        self._connect_to_events()
    

    def _connect_to_events(self):
        self.event_bus.state_persistance_manager_event_bus.writeStateRequested.connect(self.save_current_pipeline_graph)
    

    @property
    def preview_image_path(self):
        return self._preview_image_path


    def set_preview_image_path(self, path: str):
        if path and os.path.exists(path):
            self._preview_image_path = path
            self.own_event_bus.previewImagePathChanged.emit(self._preview_image_path)
    

    def set_output_node(self, node: NodeBase):
        if not self.executor.output_node:
            self.executor.output_node = node
        else:
            node.remove_post_create = True
            print("Warning: Attempted to add new instance of pipeline output node to the same graph")
            

    def set_new_active_pipeline(self, new_active_pipeline: PipelineUnit):
        if self._current_active_pipeline: 
            self.save_current_pipeline_graph()
        
        self._current_active_pipeline = new_active_pipeline

        graph_path = self._current_active_pipeline.graph_path

        self.executor.clear_output_node()
            
        if graph_path and os.path.exists(graph_path):
            self.pyflow_instance.loadFromFile(graph_path)
        else:
            self.pyflow_instance.newFile()

    
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
        base_path = os.path.join(project_path, PIPELINES_DIR_RELATIVE_PATH)
        unique_path = os.path.join(base_path, f"{base_file_name}.{self.PYFLOW_GRAPH_FILE_EXTENSION}" )
        sufix_index = 1

        while os.path.exists(unique_path):
            unique_path = os.path.join(base_path, f"{base_file_name} ({sufix_index}).{self.PYFLOW_GRAPH_FILE_EXTENSION}")
            sufix_index += 1

        return unique_path
