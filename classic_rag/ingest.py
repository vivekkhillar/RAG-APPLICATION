from typing import Any
import json
from ingestion.loader import Load_pdf
from ingestion.splitter import splitter_text
from ingestion.image_handler import image_handler
from vectorstore.embeed_store import embeed_vector_store
from config.logger import logger

class ingest():

    def __init__(self) -> None:
        
        self.doc_load = Load_pdf()
        self.chunk_per_page = splitter_text()
        self.image_processing = image_handler()
        self.embed_store = embeed_vector_store()
        self.logger = logger

    def run(self):
        
        self.logger.info("Executing the PipeLine Loading the Document")

        # Loading the PDF Document where load Function will return the Text and Image within a map where the page number will be the key 
        loaded_doc = self.doc_load.load()
        
        # After the Map will save in the loaded_doc and sending to the splitter function where all the text will be converted to chunks on the basis of the overlap and chunk size
        chunk_data_document = self.chunk_per_page.splitter(loaded_doc)
        # self.logger.info("Adding the chunk per page to the chunk_Text")

        # For debuggin purpose just check if all the chunks were came or not                
        # for chunks in chunk_data_document:
        #     self.logger.debug(chunks)
        
        # Now the same way the extracted images will send to the easyocr to find out if the image is having any text value or not that will be included into the metadata and store against the page_content
        # Also the images sent to the Lallava for the description of the image and combined with the metadata and documents

        image_data_documents = self.image_processing.image_documents(loaded_doc)

        # Invoke the embedder to embedding all the documents
        all_documents = chunk_data_document + image_data_documents
        # self.logger.info(f'Length of all documents are: {len(all_documents)}')

        vector_store = self.embed_store.vector_store(all_documents)
        self.logger.info(f'printing the vector_store {vector_store}')
        self.logger.info(f'Embedded Details were to send in the vector data base are: {len(all_documents)}')
        # Store the embbed_details to the vector data base
        
        
        return "Pipeline Executed Successfully"

        

if __name__ == "__main__":
    pipeline = ingest()
    print (pipeline.run())
    


