import numpy as np
import cv2

class Inpainter:
    def __init__(self,  expand_px = 7):
        self.expand_px = expand_px

    def inpaint_bboxes(self, image, bboxes):
        image_for_inpainting = image.copy()
        mask = np.zeros(image_for_inpainting.shape[:2], dtype=np.uint8)  # single-channel mask

        for box in bboxes:
            x_min, y_min, x_max, y_max = box

            # Expand each side safely
            x_min_exp = max(x_min - self.expand_px, 0)
            x_max_exp = min(x_max + self.expand_px, image_for_inpainting.shape[1])
            y_min_exp = max(y_min - self.expand_px, 0)
            y_max_exp = min(y_max + self.expand_px, image_for_inpainting.shape[0])

            # Draw on inpaint mask
            cv2.rectangle(mask, (x_min_exp, y_min_exp), (x_max_exp, y_max_exp), 255, -1)

        inpainted_image = cv2.inpaint(image_for_inpainting, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

        return inpainted_image