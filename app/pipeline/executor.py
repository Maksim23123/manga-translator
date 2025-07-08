from image_importer import ImageImporter
import os
import matplotlib.pyplot as plt
import cv2
from text_detector.text_detector import TextDetector

def main():
    file_name = "p (1)"
    file_ext = "jpg"
    input_folder_path = "app/data/inputs"
    image_path = os.path.join(input_folder_path, f"{file_name}.{file_ext}")

    image_importer = ImageImporter()
    if not image_importer.import_image(image_path):
        return
    original_image = image_importer.imported_image

    # Display image for test
    #---
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")
    plt.show()
    #---

    text_detector = TextDetector()

    hierarchy = text_detector.get_detection_hierarchy(original_image)

    # Display hierarchy for test
    #---
    import json
    print(json.dumps(hierarchy.hierarchy, indent=2))
    #---



if __name__ == '__main__':
    main()