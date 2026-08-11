from langchain_core.documents.base import Document
from importlib import metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import Settings
from langchain_core.documents import Document
from config.logger import logger
from BASE_DIR.directory import Directory
import json

class splitter_text: 

    def __init__(self) -> None:

        # If object is already present in the file then don't need to specify () it only required when you call any class
        self.chunk_size = Settings().CHUNK_SIZE
        self.source = Settings().DOCS_PATH
        self.CHUNK_OVERLAP = Settings().CHUNK_OVERLAP
        self.logger = logger
        self.splitter_model = RecursiveCharacterTextSplitter(chunk_size= self.chunk_size, chunk_overlap=self.CHUNK_OVERLAP)


    def splitter(self,args):
              
        self.logger.info('Now Splitting the Text into the chunks: ')

        chunk_data = []

        for i in args:
            
            if args[i]["Text"] == "":
                self.logger.warning(f"Page number {i} is not having any Text to convert into chunks")
                continue
            
            DOC = Document(
                metadata = {
                    "source" : self.source,
                    "type" : "text",
                    "page" : i
                },
                page_content = args[i]["Text"]
            )
            
            self.logger.info(f'Length of text for page {i} is : {len(args[i]['Text'])}')
            small_chunk = self.splitter_model.split_documents([DOC])
            self.logger.info(f'Page {i} having {len(small_chunk)} chunks')
            chunk_data.extend(small_chunk)

        return chunk_data

if __name__ == "__main__":

    splitter_text = splitter_text("","")
    print (splitter_text)

