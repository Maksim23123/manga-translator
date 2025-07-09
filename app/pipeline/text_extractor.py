from manga_ocr import MangaOcr
from PIL import Image
import numpy as np

class TextExtractor:
    def __init__(self):
        pass


    def _extract_text_from_leafs(self, image_np, leaf_objects):
        text_data = []
        mocr = MangaOcr()

        for obj in leaf_objects:
            x_min, y_min, x_max, y_max = obj["bbox"]

            # Crop from the original image
            crop = image_np[y_min:y_max, x_min:x_max]
            if crop.size == 0:
                continue  # Skip empty crops safely

            # Convert to PIL image
            crop_pil = Image.fromarray(crop)

            # Run OCR
            ocr_text = mocr(crop_pil)

            # Create result entry
            text_entry = {
                "parent_bbox": obj["parent_bbox"],
                "bbox": obj["bbox"],
                "translation": {
                    "original": ocr_text,
                    "translation": ""
                }
            }
            text_data.append(text_entry)

        return text_data
    

    def extract_text(self, image: np.ndarray, hierarchy) -> dict:
        return self._extract_text_from_leafs(image, hierarchy.text_chanks)