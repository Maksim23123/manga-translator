from PySide6.QtCore import QObject, Signal

class EventBus(QObject):
    activeProjectChanged = Signal(str)      # e.g. path to opened project