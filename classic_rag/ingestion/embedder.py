from config.settings import settings
from langchain_ollama import ChatOllama

class embedding:

    def __init__(self):
        self.embedding_model = settings.EMBEDDING_MODEL
    

    def embbed_image_text(self, documents):
        
        for i in documents:
            print (f'for the itteration {i}')

