from ..event_bus import EventBus
from ..context import Context
import os
import json
from datetime import datetime
from .unit import Unit

class UnitManager:

    DEFAULT_UNITS_DIR_PATH = "units"

    def __init__(self, event_bus: EventBus, context: Context):
        super().__init__()
        self.event_bus = event_bus
        self.context = context
        self.active_unit = None
        self._init_units_folder_path()


    def _init_units_folder_path(self):
        root_path = self.context.active_project_directory
        if root_path and os.path.exists(root_path):
            self.base_path = os.path.join(root_path, self.DEFAULT_UNITS_DIR_PATH)
            os.makedirs(self.base_path, exist_ok=True)


    def create_new_unit(self, unit_name, set_new_active=True):

        unit_path = os.path.join(self.base_path, unit_name)

        if os.path.exists(unit_path):
            raise FileExistsError(f"Unit folder '{unit_path}' already exists.")
        
        os.makedirs(unit_path)

        metadata = {
            "unit_name": unit_name,
            "created_at": datetime.now().isoformat(),
        }

        meta_file = os.path.join(unit_path, "unit.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"Unit '{unit_name}' created at {unit_path}")
        if set_new_active: self.load_unit(unit_path)
        return unit_path
    

    def load_unit(self, unit_path) -> bool:
        meta_file = os.path.join(unit_path, "unit.json")

        if not os.path.exists(meta_file):
            raise FileNotFoundError(f"Metadata not found at {meta_file}")
        with open(meta_file, "r", encoding="utf-8") as f:
            unit_data = json.load(f)

        if unit_data:
            self.active_unit = Unit(unit_data)
            return True
        return False