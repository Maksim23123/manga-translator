from core.core import Core
from gui.gui import GUI
from .project_window_controller import ProjectWindowController
from .unit_composer_controller.unit_composer_controller import UnitComposerController
from .pyflow_wrapper_controller.PyFlow_wrapper_controller import PyFlowWrapperController
from .page_editor_controller import PageEditorController

class Contorller:
    def __init__(self, core: Core, gui: GUI):
        self.core = core
        self.gui = gui
        self.init_controllers()
        print("Manga Translator controller initialized.")
    

    def init_controllers(self):
        self.project_window_controller = ProjectWindowController(self.core, self.gui.project_window)
        self.unit_composer_controller = UnitComposerController(self.core, self.gui.project_window.unit_composer)
        self.pyflow_wrapper_controller = PyFlowWrapperController(self.gui.project_window.pipline_editor)
        self.page_editor_controller = PageEditorController(self.gui.project_window.page_editor)
