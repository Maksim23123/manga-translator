from PyFlow.Packages.MangaTranslator.Tools.PreviewShelfTool import PreviewShelfTool

from core.core import Core



class PreviewShelfToolController:
    def __init__(self, preview_shelf_tool: PreviewShelfTool):
        self.preview_shelf_tool = preview_shelf_tool
        self.core = Core()

        self._connect_controller()
    

    def _connect_controller(self):
        self.preview_shelf_tool.triggered.connect(self._on_preview_shelf_tool_triggered)
    

    def _on_preview_shelf_tool_triggered(self):
        pipeline_executor = self.core.pipelines_manager.pyflow_interaction_manager.executor

        pipeline_executor.get_output()