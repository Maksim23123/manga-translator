from qtpy import QtGui

from PyFlow.UI.Tool.Tool import DockTool


class PipelinePropertiesDockTool(DockTool):
    """docstring for History tool."""
    def __init__(self):
        super(PipelinePropertiesDockTool, self).__init__()


    @staticmethod
    def getIcon():
        return QtGui.QIcon(":brick.png")

    @staticmethod
    def toolTip():
        return "Displays properties of current active pipeline"

    @staticmethod
    def name():
        return "Pipeline Properties"
