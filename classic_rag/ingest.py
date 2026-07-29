from typing import Any
from ingestion.loader import Load_pdf
from ingestion.splitter import splitter_text
from config.logger import logger

class ingest():

    def __init__(self) -> None:
        
        self.doc_load = Load_pdf()
        self.chunk_per_page = splitter_text()
        self.logger = logger

    def run(self):
        
        self.logger.info("Executing the PipeLine Loading the Document")
        
        loaded_doc = self.doc_load.load()
        # self.logger.info(loaded_doc)
        
        chunk_text = self.chunk_per_page.splitter(loaded_doc)
        # self.logger.filter
        
        return "Pipeline Executed Successfully"

        

if __name__ == "__main__":
    pipeline = ingest()
    print (pipeline.run())
    


