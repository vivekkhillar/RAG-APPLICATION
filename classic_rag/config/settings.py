from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from BASE_DIR.directory import Directory

# Create a Object which will direct call from the Base_dir file and found the path where the code is running
Directory = Directory()
BASE_DIR = Directory.dir()
# print (f"Print the Enviorment Base location which also can be hide : {BASE_DIR/'.env'}")
ENV_FILE= BASE_DIR/ ".env"

class Settings(BaseSettings):

    # model_config is how you tell pydantic how the class should behave not how the data it holds
    # env_file inside the settingsConfigDict read values from .env file
    # env_file_encoding Read the file as UTF-8 text
    # settgingsConfigDict will mapp below key to the model_config as the key value pair and dictionary will be model_config
    # SettingsConfigDict — tells it which .env file to use and how to read it

    model_config = SettingsConfigDict(
        env_file= ENV_FILE,
        env_file_encoding= "utf-8"
    )
    
    # BaseSettings — turns env/config into a Python object with typed fields

    OLLAMA_URL: str
    OLLAMA_MODEL: str
    VISION_MODEL: str
    EMBEDDING_MODEL: str
    CHROMA_HOST: str
    CHROMA_COLLECTION: str
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    RETRIEVER_K: int
    DOCS_PATH: str
    IMAGES_PATH: str
    LOGS_PATH: str    
    ENVIORMENT: str
    LOG_LEVEL: str
    ocr_texfinding_confidence_level: float
    PREPROCESSED_IMAGE_TEMP_PATH: str
    MAXIMUM_IMAGE_PROCESS_level: int
    VISION_MODEL_TEMPERATURE: float

    
settings = Settings()



# .env file
#    ↓
# model_config says: "read this file"
#    ↓
# Pydantic maps keys → fields (OLLAMA_URL → OLLAMA_URL)
#    ↓
# Validates types (str, int, ...)
#    ↓
# Creates settings object