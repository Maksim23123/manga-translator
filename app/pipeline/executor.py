from image_importer import ImageImporter
import os
import matplotlib.pyplot as plt
import cv2
from text_detector.text_detector import TextDetector
from text_extractor import TextExtractor
from Translator import Translator

def main():
    file_name = "p (1)"
    file_ext = "jpg"
    input_folder_path = "app/data/inputs"
    image_path = os.path.join(input_folder_path, f"{file_name}.{file_ext}")

    image_importer = ImageImporter()
    if not image_importer.import_image(image_path):
        return
    original_image = image_importer.imported_image

    text_detector = TextDetector()

    hierarchy = text_detector.get_detection_hierarchy(original_image)

    text_extractor = TextExtractor()

    extracted_text = text_extractor.extract_text(original_image.copy(), hierarchy)

    translator = Translator()

    translation_map = translator.translate_batch(extracted_text)

    # Dispaly translation map for test
    # ---
    print(translation_map)
    # ---


if __name__ == '__main__':
    main()