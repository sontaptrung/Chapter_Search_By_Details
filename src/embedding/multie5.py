import requests
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from transformers import AutoTokenizer

class MultilingualE5Large(HuggingFaceEndpointEmbeddings):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)
    def calculate_token(cls, text):
        url = f"{cls.model}/tokenize"
        payload = {"inputs": text}
        print(f"--------{text}")
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return len(response.json()[0])
        except requests.exceptions.RequestException as e:
            print(f"----------Error: {e}")
            return None
    
