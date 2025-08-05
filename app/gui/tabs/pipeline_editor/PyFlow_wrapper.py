from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QHBoxLayout, QLabel,
    QLineEdit, QListView, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from PyFlow.App import PyFlow
from PyFlow.Packages.MangaTranslator.Tools.PreviewShelfTool import PreviewShelfTool
from PyFlow.Packages.MangaTranslator.Tools.PreferencesShelfTool import PreferencesShelfTool
from PyFlow.Packages.MangaTranslator.Tools.ToolsMenuShelfTool import ToolsMenuShelfTool
from PyFlow.Packages.MangaTranslator.Tools.PluginsShelfTool import PluginsShelfTool
from PyFlow.Packages.MangaTranslator.Tools.InformationShelfTool import InformationShelfTool
from PyFlow.UI.Tool.Tool import ShelfTool, ToolBase
from core.core import Core



class PyFlowWrapper(QWidget, QObject):

    SOFTWARE = "manga-translator"

    modifiedChanged = Signal(bool)

    def __init__(self, parent: QWidget|None=None):
        super().__init__(parent)
        self.core = Core()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self._setup_pyflow()

        self.main_layout.addWidget(self.pyflow_instance)

    
    def _setup_pyflow(self):
        self.pyflow_instance = self.core.pipelines_manager.pyflow_instance

        self._remove_empty_shelf_tools()
        
        self._pull_pyflow_tools()

        self._wrap_modified_property()

        self.pyflow_instance.getMenuBar().hide()
        
    

    def _wrap_modified_property(self):

        original_modified_setter = type(self.pyflow_instance).modified.fset

        def modified_setter_wrapper(instance, value):
            old_value = instance.modified

            original_modified_setter(instance, value)

            if old_value != value:
                self.modifiedChanged.emit(value)

        type(self.pyflow_instance).modified = type(self.pyflow_instance).modified.setter(modified_setter_wrapper)

    
    def _pull_pyflow_tools(self):
        # Expose tools from MangaTranslator package for interaction
        pyflow_tools = self.pyflow_instance.getRegisteredTools()

        self.preview_shelf_tool = None
        self.preferences_shelf_tool = None
        self.tools_menu_shelf_tool = None
        self.plugins_shelf_tool = None
        self.information_shelf_tool = None

        for tool in pyflow_tools:
            if str(type(tool)) == str(PreviewShelfTool):
                self.preview_shelf_tool = tool
            
            if str(type(tool)) == str(PreferencesShelfTool):
                self.preferences_shelf_tool = tool
            
            if str(type(tool)) == str(ToolsMenuShelfTool):
                self.tools_menu_shelf_tool = tool
            
            if str(type(tool)) == str(PluginsShelfTool):
                self.plugins_shelf_tool = tool
            
            if str(type(tool)) == str(InformationShelfTool):
                self.information_shelf_tool = tool


    def _remove_empty_shelf_tools(self):
        # Remove empty shelf tools
        shelf_tool_example_instance = ShelfTool()

        #   Unrefgister empty shelf tools
        empty_shelf_tools = [instance for instance in self.pyflow_instance.getRegisteredTools() 
                             if type(instance).__name__ == type(shelf_tool_example_instance).__name__]
        for empty_shelf_tool in empty_shelf_tools:
            self.pyflow_instance.unregisterToolInstance(empty_shelf_tool)

        #   Remove empty shelftool actions
        tool_bar = self.pyflow_instance.getToolbar()
        tool_bar_actions = tool_bar.actions()
        empty_tool_actions = [action for action in tool_bar_actions if action.text() == shelf_tool_example_instance.name()]
        for empty_tool_action in empty_tool_actions:
            tool_bar.removeAction(empty_tool_action)