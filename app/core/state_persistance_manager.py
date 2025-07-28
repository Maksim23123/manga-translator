from core.event_bus.event_bus import EventBus



class StatePersistanceManager:
    """This class supposed to manage data persistance between sessions.
    It watches for changes in data of current project. And it can notify other classes
    to write their data to files."""
    
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.own_event_bus = event_bus.state_persistance_manager_event_bus
        self._data_modified = False
        self._connect_to_events()
    

    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self._clear_state)


    @property
    def data_modified(self):
        """This attribute supposed to be set only through _set_data_modified method."""
        return self._data_modified
    

    def _set_data_modified(self, value):
        """self._data_modified should be set only through this method."""
        if self.data_modified != value:
            self._data_modified = value
            self.own_event_bus.projectDataStateChanged.emit(value)


    def notify_data_modified(self):
        """If this method called project is considered to have unsaved changes."""
        self._set_data_modified(True)
    

    def save_project_data(self):
        """When this method is called all changes in the project supposed to be and
        are considered saved to files. Project transits in saved state."""
        self.own_event_bus.writeStateRequested.emit()
        self._clear_state()
    

    def _clear_state(self):
        self._set_data_modified(False)
