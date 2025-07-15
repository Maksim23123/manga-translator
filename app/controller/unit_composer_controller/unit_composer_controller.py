from core.core import Core
from gui.tabs.unit_composer.unit_composer import UnitComposer
from .unit_list.new_unit_dialog_contorller import NewUnitDialogController
from gui.tabs.unit_composer.unit_list.unit_creation_dialog import UnitCreationDialog
from .unit_list.unit_list_item_controller import UnitListItemController 

class UnitComposerController:
    def __init__(self, core: Core, unit_composer: UnitComposer):
        self.core = core
        self.unit_composer = unit_composer
        self.unit_item_controller_list = []

    
        self._connect_controller()

        self._update_unit_item_controller_list()
    

    def _connect_controller(self):
        self.unit_composer.new_unit_button.clicked.connect(self._new_unit_on_click)
        self.unit_composer.unit_list_updated.connect(self._update_unit_item_controller_list)


    def _update_unit_item_controller_list(self):
        self.unit_item_controller_list.clear()

        for item_widget in self.unit_composer.unit_item_widget_list:
            item_contorller = UnitListItemController(self.core, item_widget)
            self.unit_item_controller_list.append(item_contorller)


    def _new_unit_on_click(self):
        unit_creation_dialog = UnitCreationDialog()
        controller = NewUnitDialogController(unit_creation_dialog, self.core.unit_manager)
        unit_creation_dialog.exec()
