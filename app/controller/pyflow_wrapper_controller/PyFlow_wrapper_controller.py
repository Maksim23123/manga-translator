from core.core import Core

from gui.tabs.pipeline_editor.PyFlow_wrapper import PyFlowWrapper

from .preview_shelf_tool_controller import PreviewShelfToolController



class PyFlowWrapperController:
    def __init__(self, pyflow_wrapper: PyFlowWrapper):
        self.pyflow_wrapper = pyflow_wrapper
        self.core = Core()

        self._init_subcontrollers()
        self._connect_controller()

    
    def _connect_controller(self):
        self.pyflow_wrapper.modifiedChanged.connect(self._on_modified_changed)


    def _init_subcontrollers(self):
        preview_shelf_tool = self.pyflow_wrapper.preview_shelf_tool
        if preview_shelf_tool:
            self.preview_shelf_tool_controller = PreviewShelfToolController(preview_shelf_tool)
    

    def _on_modified_changed(self, value: bool):
        if value:
            self.core.state_persistance_manager.notify_data_modified()