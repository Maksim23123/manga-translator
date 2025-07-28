from PySide6.QtCore import QObject, Signal

from .pipeline_manager.pipeline_manager_event_bus import PipelineManagerEventBus
from .state_persistance_manager_event_bus import StatePersistanceManagerEventBus



class EventBus(QObject):
    activeProjectChanged = Signal(str)      # e.g. path to opened project
    unitsUpdated = Signal()
    activeUnitUpdated = Signal()
    activeUnitChanged = Signal()

    def __init__(self):
        super().__init__()

        self.pipeline_manager_event_bus = PipelineManagerEventBus()
        self.state_persistance_manager_event_bus = StatePersistanceManagerEventBus()