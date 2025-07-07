import yaml
from inference import get_model
import supervision as sv
import numpy as np
from PIL import Image

class InferenceDetector:
    def __init__(self):
        self._inference_api_key = None
        self.__default_api_keys_file_path = "app/config/api_keys.yaml"
        self.load_api_key(self.__default_api_keys_file_path)
        self.load_model()
        

    def load_api_key(self, api_keys_file_path):
        try:
            with open(api_keys_file_path, 'r') as file:
                api_keys_content = yaml.safe_load(file)
            
            api_keys = api_keys_content['api_keys']
            self._inference_api_key = api_keys['inference_api_key']
        except:
            print("Error:Failed to load api key")


    def load_model(self):
        try:
            if self._inference_api_key:
                self.model = get_model(model_id="manga-text-detection-xyvbw/2", api_key=self._inference_api_key)
            else:
                self.model = get_model(model_id="manga-text-detection-xyvbw/2")
        except:
            print("Error:Failed to load model")


    def detect_text(self, image: np.ndarray) -> dict:
        if self.model:
            results = self.model.infer(image)[0]
            return sv.Detections.from_inference(results)
        else:
            print("Error:Model wasn't loaded")
        return dict()