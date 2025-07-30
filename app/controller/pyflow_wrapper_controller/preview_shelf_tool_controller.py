from PyFlow.Packages.MangaTranslator.Tools.PreviewShelfTool import PreviewShelfTool



class PreviewShelfToolController:
    def __init__(self, preview_shelf_tool: PreviewShelfTool):
        self.preview_shelf_tool = preview_shelf_tool

        self._connect_controller()
    

    def _connect_controller(self):
        self.preview_shelf_tool.triggered.connect(lambda: print("It works!"))