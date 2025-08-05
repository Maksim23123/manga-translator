from core.core import Core

from gui.tabs.pipeline_editor.PyFlow_wrapper import PyFlowWrapper

from .preview_shelf_tool_controller import PreviewShelfToolController
from .preferences_shelf_tool_controller import PreferencesShelfToolController



class PyFlowWrapperController:
    def __init__(self, pyflow_wrapper: PyFlowWrapper):
        self.pyflow_wrapper = pyflow_wrapper
        self.core = Core()

        self._init_subcontrollers()
        self._connect_controller()
        self._connect_to_events()

        self._update_editor_enabled()
    

    def _connect_to_events(self):
        self.core.event_bus.pipeline_manager_event_bus.activePipelineChanged.connect(self._update_editor_enabled)

    
    def _connect_controller(self):
        self.pyflow_wrapper.modifiedChanged.connect(self._on_modified_changed)


    def _init_subcontrollers(self):
        preview_shelf_tool = self.pyflow_wrapper.preview_shelf_tool
        if preview_shelf_tool:
            self.preview_shelf_tool_controller = PreviewShelfToolController(preview_shelf_tool)

        preferences_shelf_tool = self.pyflow_wrapper.preferences_shelf_tool
        if preferences_shelf_tool:
            self.preferences_shelf_tool_controller = PreferencesShelfToolController(preferences_shelf_tool)
    

    def _on_modified_changed(self, value: bool):
        if value:
            self.core.state_persistance_manager.notify_data_modified()
    

    def _update_editor_enabled(self):
        pyflow_instance = self.core.pipelines_manager.pyflow_instance
        active_pipeline = self.core.pipelines_manager.active_pipeline

        if active_pipeline:
            pyflow_instance.canvasWidget.setEnabled(True)
        else:
            pyflow_instance.canvasWidget.setEnabled(False)