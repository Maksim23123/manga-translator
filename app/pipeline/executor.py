from image_importer import ImageImporter
import os
import matplotlib.pyplot as plt
import cv2
from text_detector.text_detector import TextDetector
from text_extractor import TextExtractor
from translator import Translator
from inpainter import Inpainter
from text_inserter import TextInserter


def main():
    file_name = "p (3)"
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

    inpainter = Inpainter()

    inpainted_image = inpainter.inpaint_bboxes(original_image.copy(), hierarchy.leaf_deepest_boxes)

    text_inserter = TextInserter()

    final_image = text_inserter.insert_text_into_image(inpainted_image, translation_map)
    
    # Display inpainted image for test
    #---
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB))
    plt.title("Result image")
    plt.axis("off")
    plt.show()
    #---

    

if __name__ == '__main__':
    main()