import chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config.settings import settings
from config.logger import logger


class retriver_builder:

    def __init__(self) -> None:
        
        self.embedding_model = OllamaEmbeddings(model = settings.EMBEDDING_MODEL, base_url= settings.OLLAMA_URL )
        self.chroma_client = chromadb.HttpClient(host = settings.CHROMA_HOST,port = settings.CHROMA_PORT)
        self.vector_store = Chroma(collection_name=settings.CHROMA_COLLECTION,embedding_function=self.embedding_model,client= self.chroma_client)
        self.logger = logger

    def get_retriver(self):

        self.logger.info('Returning the retriver Function')
        return self.vector_store.as_retriever(
            search_type = "mmr",
            search_kwargs = {"k": settings.RETRIEVER_K}
        )

        