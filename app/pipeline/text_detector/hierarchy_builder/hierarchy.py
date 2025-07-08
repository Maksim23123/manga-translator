class Hierarchy:
    def __init__(self, hierarchy: dict):
        self._hierarchy = hierarchy
        self._leaf_objects = None


    @property
    def hierarchy(self) -> dict:
        return self._hierarchy.copy()
    

    @property
    def leaf_objects(self):
        if self._leaf_objects:
            return self._leaf_objects
        else:
            self._leaf_objects = self._collect_leaf_objects(self._hierarchy)
            return self._leaf_objects

    @property
    def leaf_deepest_boxes(self):
        return self.extract_deepest_bboxes(self.leaf_objects)


    def _collect_leaf_objects(self, hierarchy):
        collected = []

        def collect_from_node(node, parent=None):
            new_node = node.copy()
            if not parent is None: new_node['parent_bbox'] = parent['bbox']
            else: new_node['parent_bbox'] = None
            # Case 1: direct children of text_bubble
            if not parent is None and parent['type'] == "text_bubble":
                collected.append(new_node)
            # Case 2: standalone clean_text, messy_text, or text_area
            elif parent is None and node["type"] in ["clean_text", "messy_text", "text_area"]:
                collected.append(new_node)
            # Recursive call for children
            for child in node.get("children", []):
                collect_from_node(child, node)

        for node in hierarchy:
            collect_from_node(node)

        return collected
    

    def extract_deepest_bboxes(self, hierarchy):
        deepest_bboxes = []

        for i in hierarchy:
            if len(i['children']) > 0:
                deepest_bboxes = deepest_bboxes + self.extract_deepest_bboxes(i['children'])
            else:
                deepest_bboxes.append(i['bbox'])

        return deepest_bboxes
