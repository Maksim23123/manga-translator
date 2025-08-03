from PyFlow.Core.GraphManager import GraphManager
from PyFlow.Core.NodeBase import NodeBase



class PipelineExecutor:
    def __init__(self, graph_manager: GraphManager):
        self._graph_manager = graph_manager
        self._output_node = None

        graph_manager.getAllNodes()

        
    @property
    def output_node(self) -> NodeBase|None:
        return self._output_node
    

    @output_node.setter
    def output_node(self, value: NodeBase):
        if not issubclass(type(value), NodeBase):
            raise TypeError(f"Expected {NodeBase.__name__} subclass, got {type(value).__name__}")
        
        self.clear_output_node()
        
        self._output_node = value

        if self._output_node:
            self._output_node.killed.connect(self.clear_output_node)
        

    def clear_output_node(self, *_):
        if self._output_node:
            self.output_node.killed.disconnect(self.clear_output_node)
        self._output_node = None
    

    def check_output_node_is_valid(self) -> bool:
        if self._output_node:
            return self.node_is_in_graph(self._output_node)
        
        return False


    def node_is_in_graph(self, node: NodeBase) -> bool:
        all_nodes = self._graph_manager.getAllNodes()
        all_nodes_uids = [node.uid for node in all_nodes]
        print(all_nodes_uids)
        if node.uid in all_nodes_uids:
            return True
        else:
            return False


    def get_output(self):
        if self.check_output_node_is_valid():
            self._output_node.compute()
