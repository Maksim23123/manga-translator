from pipeline.image_importer import ImageImporter

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *



class PipelineInputImageNode(NodeBase):

    temp_image_path = "c:/Users/makss/My_projects/ABNS/Diploma/manga-translator/app/data/inputs/p (2).jpg" # Temporary image path

    def __init__(self, name):
        super(PipelineInputImageNode, self).__init__(name)

        self.image_importer = ImageImporter()

        self.image_out_pin = self.createOutputPin('Image', 'ImageArrayPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('ImageArrayPin')
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
        if not self.image_importer.import_image(self.temp_image_path):
            return
        image = self.image_importer.imported_image
        self.image_out_pin.setData(image)
