from PyFlow.Packages.MangaTranslator.Tools.PreviewShelfTool import PreviewShelfTool
from PyFlow.Packages.MangaTranslator.manga_translator_api.gui.preview_image_selection_dialog import PreviewImageSelectionDialog 
from PyFlow.Packages.MangaTranslator.manga_translator_api.controller.preview_image_selection_dialog_controller import PreviewImageSelectionDialogController 


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
        self.preview_shelf_tool.changeImageTriggered.connect(self._show_image_selection_dialog)
    

    def _on_preview_shelf_tool_triggered(self):
        
        preview_image_path = self.core.pipelines_manager.pyflow_interaction_manager.preview_image_path

        if not preview_image_path:
            self._show_image_selection_dialog()
            return

        pipeline_executor = self.core.pipelines_manager.pyflow_interaction_manager.executor

        resulting_image = pipeline_executor.get_output()

        if isinstance(resulting_image, cv2.typing.MatLike):
            plt.figure(figsize=(8, 8))
            plt.imshow(cv2.cvtColor(resulting_image, cv2.COLOR_BGR2RGB))
            plt.title("Result image")
            plt.axis("off")
            plt.show()
    
    
    def _show_image_selection_dialog(self):
        image_selection_dialog = PreviewImageSelectionDialog()
        image_selection_controller = PreviewImageSelectionDialogController(image_selection_dialog)
        dialog_result = image_selection_dialog.exec()

        if dialog_result:
            preview_image_path = image_selection_controller.selected_image_path
            self.core.pipelines_manager.pyflow_interaction_manager.set_preview_image_path(preview_image_path)

        