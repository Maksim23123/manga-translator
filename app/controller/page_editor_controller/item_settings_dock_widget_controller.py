from PySide6.QtCore import QObject, Signal
from core.unit_manager.hierarchy_node import HierarchyNode
from core.core import Core

class ItemSettingsDockWidgetController(QObject):
    def get_available_pipelines(self):
        # Fetch list of available pipelines from Core's pipelines_manager
        return self.core.pipelines_manager.pipeline_data_model.get_pipeline_names_list() if self.core.pipelines_manager.pipeline_data_model.initialized else []

    def update_pipeline_choices(self):
        try:
            self.rebuilding_pipeline_choices = True
            pipelines = self.get_available_pipelines()
            self.dock_widget.set_pipeline_choices(pipelines)
        finally:
            self.rebuilding_pipeline_choices = False
    
    settings_changed = Signal(dict)  # Emits new settings dict

    def __init__(self, dock_widget):
        super().__init__()
        self.dock_widget = dock_widget
        self.nodes = []
        self.core = Core()
        self.rebuilding_pipeline_choices = False
        self._connect_signals()

    def set_nodes(self, nodes: list[HierarchyNode]|HierarchyNode):
        # Accepts HierarchyNode or list of HierarchyNode
        if not isinstance(nodes, list):
            nodes = [nodes]
        self.nodes = nodes
        self.update_pipeline_choices()
        self._display_settings()

    def _display_settings(self):
        try:
            self.rebuilding_pipeline_choices = True
            # For now, only pipeline setting
            pipelines = [getattr(node, 'settings', {}).get('pipeline', None) for node in self.nodes]
            if len(set(pipelines)) == 1:
                value = pipelines[0]
            else:
                value = ''  # Blank if different
            self.dock_widget.set_pipeline_value(value)
        finally:
            self.rebuilding_pipeline_choices = False

    def _connect_signals(self):
        # Connect pipeline change signal from dock widget
        self.dock_widget.connect_pipeline_changed(self._on_pipeline_changed)

    def _on_pipeline_changed(self, new_value):
        if not self.rebuilding_pipeline_choices:
            for node in self.nodes:
                if not hasattr(node, 'settings') or node.settings is None:
                    node.settings = dict()
                node.settings['pipeline'] = new_value
            self.core.state_persistance_manager.notify_data_modified()
            self.settings_changed.emit({'pipeline': new_value})
