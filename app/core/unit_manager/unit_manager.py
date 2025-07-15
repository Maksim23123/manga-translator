from ..event_bus import EventBus
from ..context import Context
import os
import json
from datetime import datetime
from .unit import Unit
import shutil


class UnitManager:

    DEFAULT_UNITS_DIR_PATH = "units"
    ORIGINAL_IMAGES_DIR_PATH = "original"

    def __init__(self, event_bus: EventBus, context: Context):
        super().__init__()
        self.event_bus = event_bus
        self.context = context
        self.active_unit = None
        self._init_units_folder_path()
        self._connect_to_events()

# Initialization

    def _init_original_folder_path(self):
        if self.base_path and os.path.exists(self.base_path):
            self.base_path = os.path.join(self.base_path, self.ORIGINAL_IMAGES_DIR_PATH)
            os.makedirs(self.base_path, exist_ok=True)
        

    def _init_units_folder_path(self):
        root_path = self.context.active_project_directory
        if root_path and os.path.exists(root_path):
            self.base_path = os.path.join(root_path, self.DEFAULT_UNITS_DIR_PATH)
            os.makedirs(self.base_path, exist_ok=True)

# Unit creation

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
        if set_new_active: self.active_unit = self.load_unit(unit_path)

        self.event_bus.unitsUpdated.emit()

        return unit_path
    
# Unit loading

    def load_unit(self, unit_path) -> Unit:
        meta_file = os.path.join(unit_path, "unit.json")

        if not os.path.exists(meta_file):
            raise FileNotFoundError(f"Metadata not found at {meta_file}")
        with open(meta_file, "r", encoding="utf-8") as f:
            unit_data = json.load(f)

        return Unit(unit_data, unit_path)

# Composing unit list

    def is_unit(self, path):
        meta_file = os.path.join(path, "unit.json")

        if not os.path.exists(meta_file): return False
        return True
    

    def get_unit_list(self):
        units = [
            f for f in os.scandir(self.base_path)
            if f.is_dir() and self.is_unit(f.path)
        ]

        # Sort by creation time (newest first or oldest first)
        # units.sort(key=lambda f: f.stat().st_birthtime)  # ⬅️ Oldest to newest
        units.sort(key=lambda f: f.stat().st_birthtime, reverse=True)  # ⬅️ Newest to oldest

        return [self.load_unit(f.path) for f in units]

# Unit removal

    def delete_unit(self, unit_path: str) -> bool:
        if self.is_unit(unit_path):
            if self.active_unit and self.active_unit.unit_path == unit_path: self.active_unit = None
            shutil.rmtree(unit_path)
            self.event_bus.unitsUpdated.emit()

# import image

    def get_original_folder_path(self):
        if self.active_unit and os.path.exists(self.active_unit.unit_path):
            return os.path.join(self.active_unit.unit_path, self.ORIGINAL_IMAGES_DIR_PATH)


    def import_image(self, image_path):
        target_folder_path = self.get_original_folder_path()

        if target_folder_path:
            # Ensure target folder exists
            os.makedirs(target_folder_path, exist_ok=True)

            # Get the image filename
            filename = os.path.basename(image_path)

            # Compute full destination path
            target_path = os.path.join(target_folder_path, filename)

            # Copy the image
            shutil.copy2(image_path, target_path)

            print(f"Imported image to {target_path}")
            return target_path  # Optional: return for tracking

    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self._init_units_folder_path)