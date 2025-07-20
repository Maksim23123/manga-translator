from PySide6.QtWidgets import QFileDialog, QMessageBox
from gui.tabs.unit_composer.unit_list.unit_creation_dialog import UnitCreationDialog
from core.unit_manager.unit_manager import UnitManager
import re
import os

class NewUnitDialogController:
    # Regex pattern: allows letters, numbers, underscores, dashes, and dots
    # No leading/trailing whitespace, no forbidden characters
    _VALID_NAME_PATTERN = re.compile(
            r"^(?!^(PRN|AUX|NUL|CON|COM\d|LPT\d)$)[a-zA-Z0-9._\s-]+$"
        )


    def __init__(self, unit_creation_dialog: UnitCreationDialog, unit_manager: UnitManager):
        self.unit_creation_dialog = unit_creation_dialog
        self.unit_manager = unit_manager

        self._connect_controller()
    

    def _connect_controller(self):
        self.unit_creation_dialog.dialog_button_box.accepted.connect(self._dialog_button_box_accepted)
        self.unit_creation_dialog.dialog_button_box.rejected.connect(self.unit_creation_dialog.reject)

   

    def _dialog_button_box_accepted(self):
        unit_name = self.unit_creation_dialog.unit_name

        if not self.is_valid_unit_name(unit_name):
            self.show_warning("Invalid Manga Name", "Manga name cannot be empty or contain illegal characters.")
            return
        
        self.unit_manager.create_new_unit(unit_name)

        self.unit_creation_dialog.accept()
    
    @classmethod
    def is_valid_unit_name(cls, name: str) -> bool:

        name = name.strip()

        # Name must not be empty after stripping
        if not name:
            return False

        # Must match allowed pattern and avoid reserved names
        return cls._VALID_NAME_PATTERN.fullmatch(name) is not None
    

    def show_warning(self, title: str, message: str):
        QMessageBox.warning(self.unit_creation_dialog, title, message)