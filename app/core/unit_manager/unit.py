from .hierarchy_node import HierarchyNode

class Unit:
    def __init__(self, unit_data: dict, unit_path: str):
        self.unit_data = unit_data
        self.unit_name = unit_data["unit_name"]
        self.unit_path = unit_path


        if 'hierarchy' in unit_data.keys() and unit_data['hierarchy']:
            self.hierarchy_root = HierarchyNode.from_dict(unit_data['hierarchy'])
        else:
            self.hierarchy_root = HierarchyNode("root", 'folder')
    
    

    def to_metadata(self):
        self.unit_data["hierarchy"] = self.hierarchy_root.to_dict()
        return self.unit_data

    