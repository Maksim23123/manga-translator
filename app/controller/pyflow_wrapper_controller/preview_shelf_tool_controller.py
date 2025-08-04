from PyFlow.Packages.MangaTranslator.Tools.PreviewShelfTool import PreviewShelfTool

from core.core import Core

import cv2
import matplotlib.pyplot as plt



class PreviewShelfToolController:
    def __init__(self, preview_shelf_tool: PreviewShelfTool):
        self.preview_shelf_tool = preview_shelf_tool
        self.core = Core()

        self._connect_controller()
    

    def _connect_controller(self):
        self.preview_shelf_tool.triggered.connect(self._on_preview_shelf_tool_triggered)
    

    def _on_preview_shelf_tool_triggered(self):
        pipeline_executor = self.core.pipelines_manager.pyflow_interaction_manager.executor

        resulting_image = pipeline_executor.get_output()

        if isinstance(resulting_image, cv2.typing.MatLike):
            plt.figure(figsize=(8, 8))
            plt.imshow(cv2.cvtColor(resulting_image, cv2.COLOR_BGR2RGB))
            plt.title("Result image")
            plt.axis("off")
            plt.show()