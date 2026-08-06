from langchain_core.documents.base import Document
from importlib import metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from config.settings import settings
from BASE_DIR.directory import Directory
from langchain_core.documents import Document
from config.logger import logger
from PIL import Image,ImageEnhance,ImageFilter
import numpy as np
import easyocr,base64,os,io


class image_handler: 

    def __init__(self) -> None:

        # If object is already present in the file then don't need to specify () it only required when you call any class
        self.chunk_size = settings.CHUNK_SIZE
        self.source = settings.DOCS_PATH
        self.base_dir = Directory().dir()
        self.temp_preprocess_image_path = settings.PREPROCESSED_IMAGE_TEMP_PATH
        self.CHUNK_OVERLAP = settings.CHUNK_OVERLAP
        self.logger = logger
        self.Ocr_Model_reader = easyocr.Reader(['en'])
        self.ocr_text_confidence_score = settings.ocr_texfinding_confidence_level 
        self.maximum_process_level = settings.MAXIMUM_IMAGE_PROCESS_level
        self.vision_model = ChatOllama(model = settings.VISION_MODEL, temperature = settings.VISION_MODEL_TEMPERATURE, base_url = settings.OLLAMA_URL)

    def check_ocr_confidence(self,images,result): 
        # check all confidence score if anything fails then reprocess the image and if confidence is ohk for all then append the text and return 

        text_from_image = []
        confidence_valid = True
            
        # Looping the list from the result where find text and confidence
        for _,text,confidence in result:

            ''' if the confidence of the text is less than expectation then it will invoke the pillow to correct the image and clear the image 
            then sent back the corrected image to find the text'''
            if confidence < self.ocr_text_confidence_score:
                confidence_valid = False
                # self.logger.info(f'Low Confidence found for image path {images} reprocessing of this image required')
                break

            text_from_image.append(text)
            
        return confidence_valid, text_from_image

    def image_correct(self,i,images):
        
        img = Image.open(images)

        if i ==1:

            # convert to gray scale
            img = img.convert("L")

            # apply contrast by 1.5x
            contrast = ImageEnhance.Contrast(img)
            img = contrast.enhance(1.5)
        
        if i == 2:
            # convert to gray scale
            img = img.convert("L")

            # apply contrast by 2.0x
            contrast = ImageEnhance.Contrast(img)
            img = contrast.enhance(2.0)

            # apply sharpness  by 2.0x
            Sharpness = ImageEnhance.Sharpness(img)
            img = Sharpness.enhance(2.0)

            # Upscale 2x with LANCZOS
            width, height = img.size

            img = img.resize(
                (width * 2, height * 2),
                Image.Resampling.LANCZOS
            )
        
        if i == 3:
            # convert to gray scale
            img = img.convert("L")

            # Upscale 2x with LANCZOS
            width, height = img.size

            img = img.resize(
                (width * 3, height * 3),
                Image.Resampling.LANCZOS
            )

            # 3. Median filter - remove noise
            img = img.filter(
                ImageFilter.MedianFilter(size=3)
            )

            #  4. Binarize - pure black and white
            threshold = 128
            img = img.point(lambda pixel: 255 if pixel> threshold else 0)
    
        return img
        
    def find_text_by_OCR(self,i,images):

        # self.logger.debug(f'Reading {images} from the page {i} and checking the text inside the image')
        # invoke the ocr_model which will return the list of the text with the confidence score
        result =  self.Ocr_Model_reader.readtext(images)
        
        # If nothing found from the OCR model then return Logging null and return None
        if not result:
            self.logger.debug(f'No text detected for {images}')
        
        # If any Text is found from the OCR model then it will check if any lowconfidence found if then break the loop and reprocess the image else return the Text
        else:

            confidence_valid,text_from_image = self.check_ocr_confidence(images,result)
   
            # If all the confidence is above the thresshold then return the text simplly
            if confidence_valid:
                
                final_text = ' '.join(text_from_image)
                # self.logger.info(f" For page {i} and {images}, the text captured is {final_text}")
                return final_text

        # Now for confidence if found less than the config then re proccess the image and find the better confidence score by pillow 
        # self.logger.info(f'Initiating the reprocess of the image path {images}')
        

        last_processed_text = None

        for level in range(1, self.maximum_process_level+1):

            corrected_image = self.image_correct(level,images)
            
            # os.makedirs(f"{self.base_dir}/{self.temp_preprocess_image_path}", exist_ok=True)
            # preprocess_path = os.path.join(self.base_dir,self.temp_preprocess_image_path)
            # temp_path = os.path.join(preprocess_path,f"{images}_temp_level_{level}.png")
            # corrected_image.save(temp_path)

            preprocessed_image_result = self.Ocr_Model_reader.readtext(np.array(corrected_image))
            

            if not preprocessed_image_result:

                # self.logger.debug(f'Level {level}: 'f'No text detected for {images}')
                continue
            
            confidence_valid,updated_text_from_image = self.check_ocr_confidence(images,preprocessed_image_result)

            # If all the confidence is above the thresshold then return the text simplly

            if updated_text_from_image:
                last_processed_text = ' '.join(
                    updated_text_from_image
                )

            if confidence_valid:
                # self.logger.info(f" For page {i} and {images}, the text captured is {updated_text_from_image}")
                return last_processed_text
        
        # self.logger.warning(f'All preprocessing levels exhausted for {images}. 'f' Last processed text returned')
        
        return last_processed_text

    def encoded_the_img(self,images):

        with open(images, "rb") as image_file:
            
            # The image file is already opened in the read mode so we need to seek the end of the file to find the size of the file
            image_file.seek(0, os.SEEK_END)
            file_size = image_file.tell()
            image_file.seek(0)

            # Create a max file size for the image to be encoded
            max_file_size = 5* 1024*1024

            image = Image.open(image_file)

            # find out the size of the image
            if file_size <= max_file_size:
                
                buffer = io.BytesIO()
                image.save(buffer,format=image.format or "PNG")
            
            else:

                image = image.convert("RGB")
                buffer = io.BytesIO()
                image.save(buffer,format="JPEG",quality=85)
                compressed_size = buffer.tell()

                if compressed_size > max_file_size:
                    
                    width,height = image.size
                    ratio = min(1600/width, 1600 / height)
                    ratio = min(ratio,1)

                    new_size = (
                                    int(width * ratio),
                                    int(height * ratio)
                                )

                    image = image.resize(new_size,Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    image.save(buffer,format="JPEG",quality=85)

            # seek the buffer to the beginning of the file to read the image
            buffer.seek(0)

            # encode the image to base64
            encoded = base64.b64encode(buffer.read()).decode("utf-8")
            buffer.close()

            return encoded

    def find_vision_model_desc(self,i,image):

        # invoke the encoded_the_img function to encode the image to base64
        encoded_image = self.encoded_the_img(image)

        message = HumanMessage(
            content= [{
                "type": "text",
                "text": """
                Analyze this image and provide a detailed description.

                Include:
                - What is shown in the image
                - Any visible text
                - Tables
                - Charts
                - Graphs
                - Important numbers
                - Labels
                - Overall meaning

                Do not make up information that is not visible.
                """
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }]
        )
        
        # invoke the vision model to find the description of the image
        description = self.vision_model.invoke([message])
        self.logger.debug(f'Printing the description for the image {image} is {description.content}')
        return description.content

    def document_builder(self,i,images,get_ocr_per_image_text,get_vision_model_desc):
        
        has_ocr = bool(get_ocr_per_image_text and get_ocr_per_image_text.strip())
        has_vision_desc = bool(get_vision_model_desc and get_vision_model_desc.strip())

        if has_ocr and has_vision_desc: 
            content = f"{get_vision_model_desc} and text found from the OCR: {get_ocr_per_image_text}"
        
        elif has_vision_desc:
            content =  get_vision_model_desc
        
        elif has_ocr:
            content = f"Text found in image: {get_ocr_per_image_text}"
        
        else:
            logger.warning(f"Both empty for {images} — skipping")
            return None

        return Document(page_content=content, metadata = {
            "source" : self.source,
            "page" : i,
            "type" : "Image",
            "image_path" : images,
            "has_ocr"    : has_ocr,
            "has_llava"  : has_vision_desc
        })

    def image_documents(self,args):

        all_image_docs = []

        # Here looping all the map sending from the ingest.py
        for i in args:
            
            # if the page don't have any images then skip this 
            if not args[i]["Images"]:
                continue
            
            # if the page having any images then it will be picked and in loop
            for images in args[i]["Images"]:
                
                try:
                
                    # For each imaage it will send to the easyOCR model where found the image having any text or not 
                    get_ocr_per_image_text = self.find_text_by_OCR(i,images)
                    self.logger.debug(f'Printing the OCR_Text for the page {i} and {images} is {get_ocr_per_image_text}')

                    get_vision_model_desc = self.find_vision_model_desc(i,images)
                    self.logger.debug(f'Printing the visionmodel description for the page {i} and {images} is {get_vision_model_desc}')

                    doc = self.document_builder(i,images,get_ocr_per_image_text,get_vision_model_desc)

                    if doc is not None:
                        all_image_docs.append(doc)
                
                except Exception as e:
                    self.logger.error(f'Error in finding the text or description for the image {images} on page {i} is {e}')

        return all_image_docs

    
if __name__ == "__main__":

    image_document = image_handler()
    print (image_document)

