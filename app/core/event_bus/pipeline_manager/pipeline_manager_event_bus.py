from PySide6.QtCore import QObject, Signal

from core.pipelines_manager.pipeline_unit import PipelineUnit

from .pipeline_manager_model_event_bus import PipelineDataModelEventBus



class PipelineManagerEventBus(QObject):

    activePipelineChanged = Signal(PipelineUnit)

    def __init__(self):
        super().__init__()

        self.pipeline_data_model_event_bus = PipelineDataModelEventBus()