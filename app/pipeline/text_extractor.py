from manga_ocr import MangaOcr
from PIL import Image
import numpy as np

class TextExtractor:
    def __init__(self):
        pass


    def _compute_zone(self, text_node, expansion_ratio=0.8):
        if text_node['parent_bbox'] is not None:
            nx_min, ny_min, nx_max, ny_max = text_node['bbox']
            px_min, py_min, px_max, py_max = text_node['parent_bbox']
            x_center = (nx_min + nx_max) / 2
            y_center = (ny_min + ny_max) / 2

            x_exp = min(abs(x_center - px_min), abs(x_center - px_max)) * expansion_ratio
            y_exp = min(abs(y_center - py_min), abs(y_center - py_max)) * expansion_ratio

            return [
                int(x_center - x_exp),
                int(y_center - y_exp),
                int(x_center + x_exp),
                int(y_center + y_exp)
            ]
        return text_node['bbox']


    def extract_text(self, image_np: np.ndarray, text_chunks, expansion_ratio=0.8) -> tuple[list[dict], list[str]]:
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

            bbox_list.append(self._compute_zone(obj, expansion_ratio))
            original_text_list.append(ocr_text)

        return bbox_list, original_text_list
