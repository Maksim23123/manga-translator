import yaml
from together import Together
import json

class Translator:
    def __init__(self):
        self._together_api_key = None
        self.__default_api_keys_file_path = "app/config/api_keys.yaml"
        self._load_api_key(self.__default_api_keys_file_path)
        self._init_client()
        self.system_prompt = """
You are a professional manga translator. Your task is to translate Japanese text into fluent, natural English that preserves the tone, context, and flow of the original manga dialogue. The translation should be adapted for a native English-speaking audience while staying true to the intent and emotion of the original.

You will be provided an array of JSON objects. Each object has:
- "id": a unique integer identifier
- "original": the full content of a single manga speech bubble

Your task is to return the same array of objects, but with an added field:
- "translation": your natural English translation

⚠️ Important:
- Translate each bubble independently.
- Do NOT change the order or structure of the array.
- Return strictly valid JSON without any additional commentary or formatting.
"""
        

    def _load_api_key(self, api_keys_file_path):
        try:
            with open(api_keys_file_path, 'r') as file:
                api_keys_content = yaml.safe_load(file)
            
            api_keys = api_keys_content['api_keys']
            self._together_api_key = api_keys['together_api_key']
        except:
            print("Error:Failed to load api key")
    

    def _init_client(self):
        try:
            self._client = Together(api_key=self._together_api_key)
        except:
            print("Error:Together client initialization failed")


    def _prepare_batch_for_translation(self, text_list):
        return [
            {"id": idx, "original": entry}
            for idx, entry in enumerate(text_list)
            if entry.strip()
        ]


    def _batch_to_list(self, translated_batch, desired_size: int):
        new_list = ["" for _ in range(desired_size)]

        for i, _ in enumerate(translated_batch):
            index = translated_batch[i]["id"]
            element = translated_batch[i]["original"]
            if index < len(new_list):
                new_list[index] = element

        return new_list


    def translate_text_list(self, text_list):
        batch = self._prepare_batch_for_translation(text_list)
        user_prompt = json.dumps(batch, ensure_ascii=False, indent=2)

        response = self._client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role":"system","content":self.system_prompt}
                    ,{"role":"user","content":user_prompt}])

        raw_response_text = response.choices[0].message.content

        translated_batch = json.loads(raw_response_text)

        return self._batch_to_list(translated_batch, len(text_list))

