from PyFlow.App import PyFlow
from PySide6.QtCore import QObject, Signal
from .pipeline_unit import PipelineUnit



class PyFlowInteractionManager():
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



    def __init__(self):
        self._current_active_pipeline = None
        self.pyflow_instance = PyFlow.instance(software=self.SOFTWARE)
    

    def set_new_active_pipeline(self, new_active_pipeline: PipelineUnit):
        pass