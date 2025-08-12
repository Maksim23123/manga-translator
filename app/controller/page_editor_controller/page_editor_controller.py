from PySide6.QtGui import QAction
from gui.tabs.page_editor.page_editor import PageEditor

from core.core import Core

from .unit_view_dock_widget_controller import UnitViewDockWidgetController



class PageEditorController:
    def __init__(self, page_editor: PageEditor):
        self.page_editor = page_editor
        
        self._init_subcontrollers()
    
    
    def _init_subcontrollers(self):
        self.unit_view_dock_widget_controller = UnitViewDockWidgetController(self.page_editor)

