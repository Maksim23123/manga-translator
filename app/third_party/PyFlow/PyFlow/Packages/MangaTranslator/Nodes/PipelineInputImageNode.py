from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class PipelineInputImageNode(NodeBase):
    def __init__(self, name):
        super(PipelineInputImageNode, self).__init__(name)
        self.out = self.createOutputPin('out', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('BoolPin')
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Pipeline input'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        print("Pipeline image input compute")
        self.out.setData(True)
