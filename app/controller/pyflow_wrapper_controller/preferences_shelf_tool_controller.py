from PyFlow.Packages.MangaTranslator.Tools.PreferencesShelfTool import PreferencesShelfTool

from core.core import Core

import cv2
import matplotlib.pyplot as plt



class PreferencesShelfToolController:
    def __init__(self, preferences_shelf_tool: PreferencesShelfTool):
        self.preferences_shelf_tool = preferences_shelf_tool
        self.core = Core()

        self._connect_controller()
    

    def _connect_controller(self):
        self.preferences_shelf_tool.triggered.connect(self._on_preferences_shelf_tool_triggered)
    

    def _on_preferences_shelf_tool_triggered(self):
        self.core.pipelines_manager.pyflow_instance.showPreferencesWindow()