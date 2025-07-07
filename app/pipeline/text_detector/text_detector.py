from .inference_detector import InferenceDetector
from .hierarchy_builder.hierarchy_builder import HierarchyBuilder
import easyocr
import numpy as np
import cv2



class TextDetector:
    def __init__(self):
        self._inference_detector = InferenceDetector()
        self._hierarchy_builder = HierarchyBuilder()


    def get_detection_hierarchy(self, image: np.ndarray) -> dict:
        detections = self._inference_detector.detect_text(image)

        reader = easyocr.Reader(['ja'])
        result = reader.detect(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), link_threshold=5, text_threshold=0.3)
        easyocr_boxes = result[0][0]

        if detections and easyocr_boxes:
            return self._hierarchy_builder.create_final_hierarchy(detections, easyocr_boxes)
        else:
            print("Error:Hierarchy building failed.")
            return dict()