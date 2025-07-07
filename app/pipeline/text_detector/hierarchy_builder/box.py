class Box:
    def __init__(self, bbox, box_type):
        self.bbox = [int(x) for x in bbox]
        self.type = box_type  # 'text_bubble', 'clean_text', 'messy_text', 'text_area'
        self.children = []

    def can_be_child_of(self, parent_type):
        if self.type == "text_area":
            return parent_type in ["clean_text", "messy_text", "text_bubble"]
        elif self.type in ["clean_text", "messy_text"]:
            return parent_type == "text_bubble"
        elif self.type == "text_bubble":
            return False
        return False

    def preferred_parent_order(self):
        if self.type == "text_area":
            return ["clean_text", "messy_text", "text_bubble"]
        elif self.type in ["clean_text", "messy_text"]:
            return ["text_bubble"]
        return []

    def to_dict(self):
        return {
            "type": self.type,
            "bbox": [int(x) for x in self.bbox],
            "children": [child.to_dict() for child in self.children]
        }