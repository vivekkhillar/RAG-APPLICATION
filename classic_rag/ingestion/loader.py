from csv import reader
import fitz
from config.settings import settings
from BASE_DIR.directory import Directory

class Load_pdf():
    # Create a object of Directory to find the actual path of the file
    # assign the path to global variable so that from the class it can be accessable         
    Directory = Directory()
    DOCS_PATH = f'{Directory.dir()}/{settings.DOCS_PATH}'

    def __init__(self):
        self.path = Load_pdf.DOCS_PATH
    
    def load(self):
        
        # Read the pdf File:
        doc = fitz.open(self.path)
        
        with fitz.open(self.path) as doc:
            for i in range (len(doc)):

                page = doc.load_page(i)
                image_list = page.get_images()
                print (image_list)

      


if __name__ == "__main__":
    pdf_load = Load_pdf()
    result = pdf_load.load()
    print(result)