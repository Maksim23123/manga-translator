from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class PipelineOutputNode(NodeBase):
    def __init__(self, name):
        super(PipelineOutputNode, self).__init__(name)
        print("Output node created")
        self.inp = self.createInputPin('inp', 'BoolPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Pipeline flow'

    @staticmethod
    def keywords():
        return ['pipeline']

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        print("compute")
