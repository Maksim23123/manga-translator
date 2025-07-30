from gui.tabs.pipeline_editor.PyFlow_wrapper import PyFlowWrapper

from .preview_shelf_tool_controller import PreviewShelfToolController



class PyFlowWrapperController:
    def __init__(self, pyflow_wrapper: PyFlowWrapper):
        self.pyflow_wrapper = pyflow_wrapper

        self._init_subcontrollers()
    

    def _init_subcontrollers(self):
        preview_shelf_tool = self.pyflow_wrapper.preview_shelf_tool
        if preview_shelf_tool:
            self.preview_shelf_tool_controller = PreviewShelfToolController(preview_shelf_tool)