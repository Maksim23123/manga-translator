from ..event_bus.event_bus import EventBus
from ..context import Context
import os
import json
from datetime import datetime
from .unit import Unit
import shutil
import uuid


class UnitManager:

    DEFAULT_UNITS_DIR_PATH = "units"
    ORIGINAL_IMAGES_DIR_PATH = "original"

    def __init__(self, event_bus: EventBus, context: Context):
        super().__init__()
        self.event_bus = event_bus
        self.context = context
        self.active_unit = None #TODO: Make active item private
        self.base_path = None
        self._init_units_folder_path()
        self._connect_to_events()

# Initialization

    def _init_units_folder_path(self):
        root_path = self.context.active_project_directory
        if root_path and os.path.exists(root_path):
            self.base_path = os.path.join(root_path, self.DEFAULT_UNITS_DIR_PATH)
            os.makedirs(self.base_path, exist_ok=True)
    

    def _connect_to_events(self):
        self.event_bus.activeProjectChanged.connect(self._on_active_project_changed)
        self.event_bus.activeUnitUpdated.connect(self.update_active_unit_metadata)
    
# Internal work

    def _on_active_project_changed(self):
        self._init_units_folder_path()
        self._clear_state()

    
    def _clear_state(self):
        self.active_unit = None
        self.event_bus.activeUnitChanged.emit()

# Unit creation

    def create_new_unit(self, unit_name, set_new_active=True):
        if not self.base_path:
            return

        unit_path = os.path.join(self.base_path, unit_name)

        if os.path.exists(unit_path):
            raise FileExistsError(f"Unit folder '{unit_path}' already exists.")
        
        os.makedirs(unit_path)

        metadata = {
            "unit_name": unit_name,
            "created_at": datetime.now().isoformat(),
            "hierarchy": None
        }

        meta_file = os.path.join(unit_path, "unit.json")
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"Unit '{unit_name}' created at {unit_path}")
        if set_new_active: self.set_active(self.load_unit(unit_path)) 

        self.event_bus.unitsUpdated.emit()

        return unit_path
    
# Unit loading

    def load_unit(self, unit_path) -> Unit|None:
        meta_file = os.path.join(unit_path, "unit.json")

        if not os.path.exists(meta_file):
            raise FileNotFoundError(f"Metadata not found at {meta_file}")
        with open(meta_file, "r", encoding="utf-8") as f:
            try:
                unit_data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f"Warning: Corupted metadata located at {unit_path}")
                return None

        return Unit(unit_data, unit_path)
    

    def set_active(self, unit: Unit|None):
        if unit and self.is_unit(unit.unit_path):
            self.update_active_unit_metadata()
            self.active_unit = self.load_unit(unit.unit_path)
            self.event_bus.activeUnitChanged.emit()


    def clear_active(self):
        self.update_active_unit_metadata()
        self.active_unit = None
        self.event_bus.activeUnitChanged.emit()

# Composing unit list

    def is_unit(self, path):
        meta_file = os.path.join(path, "unit.json")

        if not os.path.exists(meta_file): return False
        return True
    

    def get_unit_list(self):
        if not self.base_path:
            return

        units = [
            f for f in os.scandir(self.base_path)
            if f.is_dir() and self.is_unit(f.path)
        ]

        # Sort by creation time (newest first or oldest first)
        # units.sort(key=lambda f: f.stat().st_birthtime)  # ⬅️ Oldest to newest
        units.sort(key=lambda f: f.stat().st_birthtime, reverse=True)  # ⬅️ Newest to oldest

        return [self.load_unit(f.path) for f in units] # TODO: Make get_unit_list function not load all the files of units on every call and cache it instead.

# Unit removal

    def delete_unit(self, unit_path: str) -> bool:
        if self.is_unit(unit_path):
            if self.active_unit and self.active_unit.unit_path == unit_path: 
                self.active_unit = None
                self.event_bus.activeUnitChanged.emit()
                return True
            shutil.rmtree(unit_path)
            self.event_bus.unitsUpdated.emit()
        return False

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
            
            if not self.active_unit:
                return

            self.active_unit.hierarchy_root.add_image(remove_extension(filename), target_path)
            self.update_active_unit_metadata()
            self.event_bus.activeUnitUpdated.emit()

            print(f"Imported image to {target_path}")
            return target_path  # Optional: return for tracking

# Unit Update

    def set_unit_name(self, new_name: str):
        if self.active_unit and new_name:
            self.active_unit.unit_name = new_name
            self.update_active_unit_metadata()
            self.event_bus.activeUnitChanged.emit()
            self.event_bus.unitsUpdated.emit()


# Update current unit meta

    def update_active_unit_metadata(self):
        if self.active_unit and self.is_unit(self.active_unit.unit_path):
            unit_path = self.active_unit.unit_path
            meta_file = os.path.join(unit_path, "unit.json")
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(self.active_unit.to_metadata(), f, indent=4)



def remove_extension(filename: str) -> str:
    return os.path.splitext(filename)[0]