from ingestion.loader import Load_pdf

class ingest():

    def __init__(self) -> None:
        
        self.doc_load = Load_pdf()
    
    def run(self):

        self.doc_load.load()

        return "Pipeline Executed Successfully"

        

if __name__ == "__main__":
    pipeline = ingest()
    print (pipeline.run())
    


