from core.core import Core
from gui.tabs.unit_composer.unit_composer import UnitComposer
from .new_unit_dialog_contorller import NewUnitDialogController
from gui.tabs.unit_composer.unit_creation_dialog import UnitCreationDialog

class UnitComposerController:
    def __init__(self, core: Core, unit_composer: UnitComposer):
        self.core = core
        self.unit_composer = unit_composer

    
        self._connect_controller()
    

    def _connect_controller(self):
        self.unit_composer.new_unit_button.clicked.connect(self._new_unit_on_click)
    

    def _new_unit_on_click(self):
        unit_creation_dialog = UnitCreationDialog()
        controller = NewUnitDialogController(unit_creation_dialog, self.core.unit_manager)
        unit_creation_dialog.exec()
