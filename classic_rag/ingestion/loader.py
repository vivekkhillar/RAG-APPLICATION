from csv import reader
from tkinter import image_types
import fitz,os,json
from config.settings import Settings
from BASE_DIR.directory import Directory
from config.logger import logger

class Load_pdf:
    
    # Create a object of Directory to find the actual path of the file
    # assign the path to global variable so that from the class it can be accessable         
    Directory = Directory()
    settings = Settings()
    DOCS_PATH = f'{Directory.dir()}/{settings.DOCS_PATH}'
    IMAGE_PATH = f'{Directory.dir()}/{settings.IMAGES_PATH}'

    def __init__(self):
        self.logger = logger
        self.path = Load_pdf.DOCS_PATH
        self.text_image_per_page_details = {}
        self.IMAGE_STORE_PATH = Load_pdf.IMAGE_PATH

    def load(self):
        
        # Read the pdf File:

        self.logger.info('Opening the PDF')
        with fitz.open(self.path) as doc: 

            self.logger.info('Loading the PDF per page to read all the text and images')

            for page_number in range (1,len(doc)+1):
                
                page = doc.load_page(page_number-1)

                # To load the text then only use get_text()
                text = page.get_text()

                # To load images then use get_images() which include the image object ID from the page 
                images = page.get_images(full= True)
                
                # To load tables then use this to update in the json extracted how many tables and sent in the map
                tables = page.find_tables()

                page_tables = []

                for table_index, table in enumerate(tables.tables, start=1):
                    
                    table_data = table.extract()
                    page_tables.append({
                        "table_number": table_index,
                        "data": table_data
                    })
                
                # create a list of page_images 
                page_images = []
                
                for image_index,img in enumerate(images):

                    # print (image_index,img)
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    # print (base_image)

                    # Find image bytes and ext 
                    image_bytes = base_image['image']
                    image_ext = base_image['ext']
                    
                    # Create a image name from which page
                    image_name = f"page_{page_number}_img_{image_index+1}.{image_ext}"

                    # create a image_path to store the iamges
                    image_unique_path = os.path.join(self.IMAGE_STORE_PATH,image_name)
                    
                    # print(image_unique_path)
                    # print (image_name)
                    
                    os.makedirs(self.IMAGE_STORE_PATH,exist_ok=True)
                    
                    with open(image_unique_path,"wb") as f:
                        f.write(image_bytes)

                    page_images.append(image_unique_path)
                
                self.text_image_per_page_details[page_number] = {"Text": text, "Images" : page_images, "tables" : page_tables}

            self.logger.info('Returning the JSON DUMP which mapped to loaded_doc')
            self.logger.info(json.dumps(self.text_image_per_page_details,indent=4))
            return self.text_image_per_page_details

if __name__ == "__main__":
    pdf_load = Load_pdf()
    result = pdf_load.load()