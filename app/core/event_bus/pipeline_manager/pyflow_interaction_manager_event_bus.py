from PySide6.QtCore import QObject, Signal

class PyFlowInteractionManagerEventBus(QObject):

    previewImagePathChanged = Signal(str)