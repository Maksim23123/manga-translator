from manga_ocr import MangaOcr
from PIL import Image
import numpy as np

class TextExtractor:
    def __init__(self):
        pass


    def extract_text(self, image_np: np.ndarray, text_chunks) -> tuple[list[dict], list[str]]:
        bbox_list = []
        original_text_list = []
        mocr = MangaOcr()

        for obj in text_chunks:
            x_min, y_min, x_max, y_max = obj["bbox"]

            # Crop from the original image
            crop = image_np[y_min:y_max, x_min:x_max]
            if crop.size == 0:
                continue  # Skip empty crops safely

            # Convert to PIL image
            crop_pil = Image.fromarray(crop)

            # Run OCR
            ocr_text = mocr(crop_pil)

            bbox_list.append(obj["bbox"])
            original_text_list.append(ocr_text)

        return bbox_list, original_text_list
