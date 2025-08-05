from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QCursor

from PyFlow.Packages.MangaTranslator.Tools.InformationShelfTool import InformationShelfTool

from core.core import Core



class InformationShelfToolController:
    def __init__(self, shelf_tool_instance: InformationShelfTool):
        self.core = Core()
        self.shelf_tool_instance = shelf_tool_instance
        self.menu = None

        self._init_tools_menu()

        self._connect_controller()
    

    def _connect_controller(self):
        self.shelf_tool_instance.triggered.connect(self._show_menu)
    

    def _init_tools_menu(self):
        menu_bar = self.core.pipelines_manager.pyflow_instance.getMenuBar()
        DEFAULT_MENU_TITLE_IN_PYFLOW = "Help"
        for child in menu_bar.findChildren(QMenu):
            if child.title() == DEFAULT_MENU_TITLE_IN_PYFLOW:
                self.menu = child
                break
    

    def _show_menu(self):
        if self.menu:
            mouse_position = QCursor.pos()
            self.menu.exec_(mouse_position)
            