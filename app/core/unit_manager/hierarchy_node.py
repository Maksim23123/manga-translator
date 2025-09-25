import uuid



class HierarchyNode:
    FOLDER_TYPE = "folder"
    IMAGE_TYPE = "image"

    def __init__(self, name, node_type, image_path=None, id=None, settings=None):
        self.id = id if id else uuid.uuid4().hex
        self.name = name
        self.type = node_type  # 'folder' or 'image'
        self.image_path = image_path  # only for image nodes
        self.children = []
        self.settings = settings if settings is not None else dict()


    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "settings": self.settings,
        }
        if self.type == self.IMAGE_TYPE:
            data["image_path"] = self.image_path
        else:
            data["children"] = [child.to_dict() for child in self.children]
        return data


    def add_image(self, name, path):
        self.children.append(HierarchyNode(name, self.IMAGE_TYPE, path))
    

    def add_folder(self, name):
        self.children.append(HierarchyNode(name, self.FOLDER_TYPE))


    @staticmethod
    def from_dict(data):
        node = HierarchyNode(
            data["name"],
            data["type"],
            data.get("image_path"),
            data.get("id"),
            data.get("settings", dict())
        )
        if node.type == HierarchyNode.FOLDER_TYPE:
            node.children = [HierarchyNode.from_dict(c) for c in data.get("children", [])]
        return node