from langchain_core.documents.base import Document
from importlib import metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import Settings
from langchain_core.documents import Document
from config.logger import logger
from BASE_DIR.directory import Directory
import json

class table_handler: 

    def __init__(self) -> None:

        # If object is already present in the file then don't need to specify () it only required when you call any class
        self.chunk_size = Settings().CHUNK_SIZE
        self.source = Settings().DOCS_PATH
        self.CHUNK_OVERLAP = Settings().CHUNK_OVERLAP
        self.logger = logger
        self.splitter_model = RecursiveCharacterTextSplitter(chunk_size= self.chunk_size, chunk_overlap=self.CHUNK_OVERLAP)


    def table_documents(self,args):
              
        self.logger.info('Now converting the tables to readable document')
        documents = []
        for page_number, page_data in args.items():
            
            tables = page_data.get("tables", [])

            # No tables on this page
            if not tables:
                self.logger.info(
                    f"Page {page_number} has no tables"
                )
                continue

            # Multiple tables can exist on one page
            for table in tables:

                table_data = table.get("data", [])

                table_number = table.get(
                    "table_number",
                    "?"
                )

                if not table_data:
                    self.logger.warning(
                        f"Page {page_number}, "
                        f"table {table_number} is empty"
                    )
                    continue

                # Convert table rows to readable text
                table_text = "\n".join(
                    " | ".join(
                        str(cell).strip()
                        if cell is not None
                        else ""
                        for cell in row
                    )
                    for row in table_data
                )

            

            DOC = Document(
                    page_content=table_text,
                    metadata={
                        "page": page_number,
                        "source": self.source,
                        "type": "table",
                        "table_number": table_number
                    }
                )
            documents.append(DOC)
            
        return documents        

if __name__ == "__main__":

    table_convert = table_handler("","")
    print (table_convert)

