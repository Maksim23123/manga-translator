from PySide6.QtCore import QObject, Signal



class StatePersistanceManagerEventBus(QObject):

    writeStateRequested = Signal()

    projectDataStateChanged = Signal(bool)


