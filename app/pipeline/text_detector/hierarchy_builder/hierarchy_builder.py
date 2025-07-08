from .box import Box
from .hierarchy import Hierarchy

class HierarchyBuilder:
    def __init__(self):
        pass

    def is_inside(self, parent_bbox, child_bbox, margin=0.5):
        px_min, py_min, px_max, py_max = [int(x) for x in parent_bbox]
        cx_min, cy_min, cx_max, cy_max = [int(x) for x in child_bbox]

        child_area = (cx_max - cx_min) * (cy_max - cy_min)

        ix_min = max(px_min, cx_min)
        iy_min = max(py_min, cy_min)
        ix_max = min(px_max, cx_max)
        iy_max = min(py_max, cy_max)

        if ix_min >= ix_max or iy_min >= iy_max:
            return False

        intersection_area = (ix_max - ix_min) * (iy_max - iy_min)
        return (intersection_area / child_area) >= margin


    def build_hierarchy(self, boxes):
        boxes = [Box(bbox=box["bbox"], box_type=box["type"]) for box in boxes]

        def find_parent(candidate, potential_parents):
            for preferred_type in candidate.preferred_parent_order():
                best_parent = None
                for parent in potential_parents:
                    if parent.type != preferred_type:
                        continue
                    if not candidate.can_be_child_of(parent.type):
                        continue
                    if self.is_inside(parent.bbox, candidate.bbox):
                        for child in parent.children:
                            deeper_parent = find_parent(candidate, [child])
                            if deeper_parent:
                                return deeper_parent
                        best_parent = parent
                if best_parent:
                    return best_parent
            return None

        hierarchy = []

        for candidate in boxes:
            parent = find_parent(candidate, hierarchy)
            if parent:
                parent.children.append(candidate)
            else:
                if candidate.type != "text_bubble":
                    parentless = find_parent(candidate, boxes)
                    if parentless:
                        parentless.children.append(candidate)
                        continue
                hierarchy.append(candidate)

        return [node.to_dict() for node in hierarchy]


    def convert_supervision_to_boxes(self, detections):
        all_boxes = []
        for bbox, cls_name in zip(detections.xyxy, detections.data['class_name']):
            box_dict = {
                "bbox": [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])],
                "type": cls_name
            }
            all_boxes.append(box_dict)
        return all_boxes


    def convert_easyocr_to_boxes(self, easyocr_boxes):
        all_boxes = []
        for box in easyocr_boxes:
            x_min, x_max = min(box[0], box[1]), max(box[0], box[1])
            y_min, y_max = min(box[2], box[3]), max(box[2], box[3])
            box_dict = {
                "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)],
                "type": "text_area"
            }
            all_boxes.append(box_dict)
        return all_boxes


    def create_final_hierarchy(self, detections, easyocr_boxes) -> Hierarchy:
        supervision_boxes = self.convert_supervision_to_boxes(detections)
        easyocr_box_data = self.convert_easyocr_to_boxes(easyocr_boxes)
        combined_boxes = supervision_boxes + easyocr_box_data
        return Hierarchy(self.build_hierarchy(combined_boxes))