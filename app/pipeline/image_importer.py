import cv2
from PIL import Image
import numpy as np

class ImageImporter:
    def __init__(self):
        self._imported_pil_image = None

    @property
    def imported_image(self):
        return cv2.cvtColor(np.array(self._imported_pil_image), cv2.COLOR_RGB2BGR)
    
    @property
    def imported_pil_image(self):
        return self._imported_pil_image.copy()

    def import_image(self, image_path: str) -> bool:
        try:
            self._imported_pil_image = Image.open(image_path).convert("RGB")
            return True
        except Exception:
            print("Error: Image import failed.")
            return False

    