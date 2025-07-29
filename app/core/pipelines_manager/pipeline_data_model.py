import inspect

from core.event_bus.event_bus import EventBus
from core.context import Context
from core.state_persistance_manager import StatePersistanceManager

from .pipeline_data import PipelineData
from .pipeline_unit import PipelineUnit



class PipelineDataModel:
    def __init__(self, event_bus: EventBus, context: Context):
        self.project_state_manager = context.state_persistance_manager
        self.own_event_bus = event_bus.pipeline_manager_event_bus.pipeline_data_model_event_bus
        self._pipeline_data = None

    
    @property
    def initialized(self):
        if self._pipeline_data:
            return True
        else:
            return False
    

    def _check_pipeline_data(self):
        if not self._pipeline_data:
            raise ValueError("Pipeline data not set. Call set_pipeline_data() first.")

    
    def get_pipeline(self, target_pipeline_name: str) -> PipelineUnit|None:
        self._check_pipeline_data()

        if not target_pipeline_name.strip():
            return None

        for pipeline in self._pipeline_data.pipelines_list:
            if pipeline.name == target_pipeline_name:
                return pipeline
    

    def _on_pipeline_updated(self, pipeline: PipelineUnit):
        pipelines_under_same_name = [same_name_pipeline for same_name_pipeline 
                                     in self._pipeline_data.pipelines_list if same_name_pipeline.name == pipeline.name]
        
        if len(pipelines_under_same_name) > 1:
            old_name = pipeline.name
            new_pipeline_name = self.generate_unique_pipeline_name(old_name)
            pipeline.name = new_pipeline_name
            print(f"Warning: Pipeline name should be unique. Name \"{old_name}\" changed to \"{pipeline.name}\"")
        
        index = self._pipeline_data.pipelines_list.index(pipeline)

        self.project_state_manager.notify_data_modified()
        self.own_event_bus.pipelineUpdated.emit(index)
    
    def remove_pipeline(self, pipeline_name: str) -> bool:
        self._check_pipeline_data()
        pipeline_to_remove = None

        for pipeline in self._pipeline_data.pipelines_list:
            if pipeline.name == pipeline_name:
                pipeline_to_remove = pipeline
                break
        
        if pipeline_to_remove:
            self._pipeline_data.pipelines_list.remove(pipeline_to_remove)
            self.own_event_bus.pipelineRemoved.emit(pipeline_to_remove)
            self.project_state_manager.notify_data_modified()
            return True
        else:
            return False
    

    def set_pipeline_data(self, pipeline_data: PipelineData) -> None:
        self._pipeline_data = pipeline_data

        for pipeline in self._pipeline_data.pipelines_list:
            pipeline.add_on_change_callable(self._on_pipeline_updated)
    

    def add_pipeline(self, pipeline_name: str) -> PipelineUnit:
        self._check_pipeline_data()

        if not pipeline_name.strip():
            raise Exception("Pipeline name can't be empty")
        
        new_pipeline_name = self.generate_unique_pipeline_name(pipeline_name)

        new_pipeline = PipelineUnit(new_pipeline_name)

        new_pipeline.add_on_change_callable(self._on_pipeline_updated)

        self._pipeline_data.pipelines_list.append(new_pipeline)

        self.own_event_bus.pipelineAdded.emit()
        self.project_state_manager.notify_data_modified()

        return new_pipeline
    

    def get_pipeline_names_list(self):
        self._check_pipeline_data()
        pipeline_names_list = list()

        for pipeline in self._pipeline_data.pipelines_list:
            pipeline_names_list.append(pipeline.name)
        
        return pipeline_names_list
    

    def generate_unique_pipeline_name(self, name_base: str):
        name_base = name_base.strip()
        unique_name = name_base
        pipeline_names_list = self.get_pipeline_names_list()
        postfix_number = 1

        while unique_name in pipeline_names_list:
            unique_name = name_base.strip() + f" ({postfix_number})"
            postfix_number += 1
        
        return unique_name
