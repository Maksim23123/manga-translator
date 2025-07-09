import cv2
import numpy as np


class TextInserter:
    def __init__(self, font = cv2.FONT_HERSHEY_SIMPLEX,
            base_font_scale = 1.0,
            color = (255, 255, 255),
            thickness = 2):
        self.font = font
        self.base_font_scale = base_font_scale
        self.color = color
        self.thickness = thickness
        


    def insert_text_into_image(self, image, text_areas, text_list):
        image_with_text = image.copy()

        def zones_intersect(a, b):
            ax1, ay1, ax2, ay2 = a
            bx1, by1, bx2, by2 = b
            return not (ax2 <= bx1 or ax1 >= bx2 or ay2 <= by1 or ay1 >= by2)

        def shrink_zone(zone, shrink_ratio):
            x1, y1, x2, y2 = zone
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            w = (x2 - x1) * shrink_ratio / 2
            h = (y2 - y1) * shrink_ratio / 2
            return [int(cx - w), int(cy - h), int(cx + w), int(cy + h)]

        def resolve_overlaps(zones, max_iters=20, shrink_step=0.95):
            n = len(zones)
            final_zones = zones[:]
            for _ in range(max_iters):
                conflict = False
                for i in range(n):
                    for j in range(i + 1, n):
                        if zones_intersect(final_zones[i], final_zones[j]):
                            final_zones[i] = shrink_zone(final_zones[i], shrink_step)
                            final_zones[j] = shrink_zone(final_zones[j], shrink_step)
                            conflict = True
                if not conflict:
                    break
            return final_zones

        def draw_wrapped_text_in_zone(img, text, zone, font, base_scale, color, thickness):
            x_min, y_min, x_max, y_max = zone
            box_width = x_max - x_min
            box_height = y_max - y_min

            def wrap_text(text, font_scale):
                words = text.split()
                lines, line = [], ""
                for word in words:
                    test_line = (line + " " + word).strip()
                    width, _ = cv2.getTextSize(test_line, font, font_scale, thickness)[0]
                    if width <= box_width:
                        line = test_line
                    else:
                        if line:
                            lines.append(line)
                        if cv2.getTextSize(word, font, font_scale, thickness)[0][0] > box_width:
                            # Even single word is too wide, force it in
                            lines.append(word)
                            line = ""
                        else:
                            line = word
                if line:
                    lines.append(line)
                return lines

            def get_text_block_size(lines, font_scale):
                if not lines:
                    return 0, 0
                (w, h), _ = cv2.getTextSize("A", font, font_scale, thickness)
                block_height = len(lines) * (h + 10)
                block_width = max(cv2.getTextSize(line, font, font_scale, thickness)[0][0] for line in lines)
                return block_width, block_height

            font_scale = base_scale
            for _ in range(30):
                lines = wrap_text(text, font_scale)
                tw, th = get_text_block_size(lines, font_scale)
                if tw <= box_width and th <= box_height:
                    break
                font_scale *= 0.95
                if font_scale < 0.2:
                    break

            # Center text
            text_start_y = y_min + (box_height - th) // 2 + int(cv2.getTextSize("A", font, font_scale, thickness)[0][1])
            for i, line in enumerate(lines):
                line_width = cv2.getTextSize(line, font, font_scale, thickness)[0][0]
                text_start_x = x_min + (box_width - line_width) // 2
                y = text_start_y + i * (cv2.getTextSize("A", font, font_scale, thickness)[0][1] + 10)
                cv2.putText(img, line, (text_start_x, y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

        # Step 1: Get and resolve text zones
        non_overlapping_zones = resolve_overlaps(text_areas)

        # Step 2: Draw text in zones
        base_image = np.zeros_like(image_with_text)
        for i, text in enumerate(text_list):
            zone = non_overlapping_zones[i]
            text = text
            draw_wrapped_text_in_zone(base_image
                                      , text, zone, self.font, base_scale=self.base_font_scale
                                      , color=self.color, thickness=self.thickness)

        # Step 3: Invert colors where white text was drawn
        mask = base_image == 255
        image_with_text[mask] = 255 - image_with_text[mask]

        return image_with_text