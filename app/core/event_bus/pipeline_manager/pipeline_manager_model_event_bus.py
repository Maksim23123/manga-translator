from PySide6.QtCore import QObject, Signal

from core.pipelines_manager.pipeline_unit import PipelineUnit



class PipelineDataModelEventBus(QObject):
    
    pipelineRemoved = Signal(PipelineUnit)
    pipelineAdded = Signal()
    pipelineUpdated = Signal(int)