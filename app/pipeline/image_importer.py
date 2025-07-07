import cv2
from PIL import Image
import numpy as np

class ImageImporter:
    def __init__(self):
        self._imported_image = None

    @property
    def imported_image(self):
        return self._imported_image.copy()

    def import_image(self, image_path: str) -> bool:
        try:
            pil_image = Image.open(image_path).convert("RGB")
            cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # For OpenCV use
            self._imported_image = cv2_image
            return True
        except Exception:
            print("Error: Image import failed.")
            return False

    