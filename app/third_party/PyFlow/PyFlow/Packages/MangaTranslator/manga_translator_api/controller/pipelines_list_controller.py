from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication, 
    QMainWindow, QMenuBar, QMenu, QTabWidget, QLabel, QListWidgetItem, QAbstractItemView
)
from core.core import Core
from ..gui.pipelines_list.pipelines_list import PipelinesList
from ..gui.pipelines_list.pipelines_list_item import PipelinesListItem
from ..gui.pipelines_list.new_pipeline_dialog import NewPipelineDialog



class PipelinesListController:

    EMPTY_ITEM_NAME = "[empty]"

    def __init__(self, pipelines_list: PipelinesList):
        self.pipelines_list = pipelines_list
        self.core = Core()
        self.pipelines_model = self.core.pipelines_manager.pipeline_data_model
        self.item_widget_list = list()

        self._connect_to_events()
        self._connect_controller()
        self.update_list_widget()


    def _connect_to_events(self):
        self.core.event_bus.activeProjectChanged.connect(self.update_list_widget)
    

    def _connect_controller(self):
        self.pipelines_list.new_pipeline_toolButton.clicked.connect(self._on_new_pipeline_button_clicked)


    def update_list_widget(self):
        self.pipelines_list.pipelines_list_listWidget.clear()
        self.item_widget_list.clear()

        active_pipeline = self.core.pipelines_manager.active_pipeline

        if self.pipelines_model.initialized:
            for item_name in self.pipelines_model.get_pipeline_names_list():
                active = True if active_pipeline and active_pipeline.name == item_name else False
                self._add_list_item(item_name, active)


    def _add_list_item(self, item_name: str, is_active: bool=False):
        item_widget = PipelinesListItem(item_name, is_active, self.pipelines_list)

        listWidget =  self.pipelines_list.pipelines_list_listWidget

        # Create a placeholder item
        item = QListWidgetItem(listWidget)
        item.setSizeHint(item_widget.sizeHint())

        listWidget.addItem(item)
        listWidget.setItemWidget(item, item_widget)

        self.item_widget_list.append(item_widget)
    

    def _on_new_pipeline_button_clicked(self):
        new_pipeline_dialog = NewPipelineDialog(self.pipelines_list)

        result = new_pipeline_dialog.exec()

        if result and self.pipelines_model.initialized:
            new_pipeline_name = new_pipeline_dialog.pipeline_name
            self.pipelines_model.add_pipeline(new_pipeline_name)

