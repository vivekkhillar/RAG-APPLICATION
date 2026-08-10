import chromadb
from config.settings import settings
from config.logger import logger
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

class embeed_vector_store:

    def __init__(self) -> None:
        
        self.logger = logger
        self.collection = settings.CHROMA_COLLECTION
        self.embedding_model = OllamaEmbeddings(model=settings.EMBEDDING_MODEL,base_url=settings.OLLAMA_URL)
        self.vector_db_client = chromadb.HttpClient(host=settings.CHROMA_HOST,port= settings.CHROMA_PORT)

    def vector_store(self,all_documents):

        vectorstore = Chroma(
            collection_name = self.PDF_name,
            embedding_function= self.embedding_model,
            client= self.vector_db_client
        )
        vectorstore.add_documents(all_documents)
        self.logger.info(f"Storing {len(all_documents)} documents in ChromaDB")
        return vectorstore