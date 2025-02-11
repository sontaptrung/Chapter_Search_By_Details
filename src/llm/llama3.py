from langchain_openai import ChatOpenAI
import requests

class Llama3Engine(ChatOpenAI):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)
    
    def calculate_token(self, text):
        url = f"{self.openai_api_base.strip('/v1')}/tokenize"
        payload = {"content": text}

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return len(response.json()["tokens"])
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
