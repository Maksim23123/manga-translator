from qtpy import QtGui

from PyFlow.UI.Tool.Tool import DockTool
from .pipelines_list.pipelines_list import PipelinesList

# TODO: Remove - Test

from .pipelines_list.pipelines_list_item import PipelinesListItem


class PipelineListDockTool(DockTool):
    """docstring for History tool."""
    def __init__(self):
        super(PipelineListDockTool, self).__init__()
        self.pipeline_list = PipelinesList(self)

        self.setWidget(self.pipeline_list)

        # TODO: Remove - Test

        self.pipeline_list_item = PipelinesListItem()

        self.pipeline_list_item.show()


    @staticmethod
    def getIcon():
        return QtGui.QIcon(":brick.png")

    @staticmethod
    def toolTip():
        return "My awesome dock tool!"

    @staticmethod
    def name():
        return "Pipeline list"
