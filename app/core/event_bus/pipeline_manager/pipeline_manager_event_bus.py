from PySide6.QtCore import QObject, Signal

from core.pipelines_manager.pipeline_unit import PipelineUnit

from .pipeline_manager_model_event_bus import PipelineDataModelEventBus
from .pyflow_interaction_manager_event_bus import PyFlowInteractionManagerEventBus



class PipelineManagerEventBus(QObject):

    activePipelineChanged = Signal(PipelineUnit)

    def __init__(self):
        super().__init__()

        self.pipeline_data_model_event_bus = PipelineDataModelEventBus()
        self.pyflow_iteraction_manager_event_bus = PyFlowInteractionManagerEventBus()