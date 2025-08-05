from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QCursor

from PyFlow.Packages.MangaTranslator.Tools.ToolsMenuShelfTool import ToolsMenuShelfTool

from core.core import Core



class ToolsMenuShelfToolController:
    def __init__(self, shelf_tool_instance: ToolsMenuShelfTool):
        self.core = Core()
        self.shelf_tool_instance = shelf_tool_instance
        self.tools_menu = None

        self._init_tools_menu()

        self._connect_controller()
    

    def _connect_controller(self):
        self.shelf_tool_instance.triggered.connect(self._show_tools_menu)
    

    def _init_tools_menu(self):
        menu_bar = self.core.pipelines_manager.pyflow_instance.getMenuBar()
        DEFAULT_TOOLS_MENU_TITLE = "Tools"
        for child in menu_bar.findChildren(QMenu):
            if child.title() == DEFAULT_TOOLS_MENU_TITLE:
                self.tools_menu = child
                break
    

    def _show_tools_menu(self):
        if self.tools_menu:
            mouse_position = QCursor.pos()
            self.tools_menu.exec_(mouse_position)
            