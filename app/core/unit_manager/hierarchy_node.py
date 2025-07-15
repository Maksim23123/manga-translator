class HierarchyNode:
    def __init__(self, name, node_type, image_path=None):
        self.name = name
        self.type = node_type  # 'folder' or 'image'
        self.image_path = image_path  # only for image nodes
        self.children = []


    def to_dict(self):
        data = {
            "name": self.name,
            "type": self.type,
        }
        if self.type == "image":
            data["image_path"] = self.image_path
        else:
            data["children"] = [child.to_dict() for child in self.children]
        return data


    def add_image(self, name, path):
        self.children.append(HierarchyNode(name, "image", path))
    

    def add_folder(self, name):
        self.children.append(HierarchyNode(name, "folder"))


    @staticmethod
    def from_dict(data):
        node = HierarchyNode(data["name"], data["type"], data.get("image_path"))
        if node.type == "folder":
            node.children = [HierarchyNode.from_dict(c) for c in data.get("children", [])]
        return node