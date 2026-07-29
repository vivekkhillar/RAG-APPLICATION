import datetime,os,logging
from ntpath import exists
from string import Formatter
from BASE_DIR.directory import Directory
from config.settings import Settings


class Logger:
    
    Directory = Directory()
    BASE_DIR = Directory.dir()
    Settings = Settings()    

    def __init__(self) -> None:
        self.Settings = Logger.Settings
        self.logger_name = "CLASSIC_RAG"
        self.log_level = Logger.Settings.LOG_LEVEL
        self.log_dir = os.path.join(Logger.BASE_DIR,Logger.Settings.LOGS_PATH)
        self.log_file = os.path.join(self.log_dir,"app.log")
        self.log_format = "%(process)-5d | %(asctime)s | %(levelname)-8s | %(filename)-8s:%(lineno)-5d | %(funcName)-8s | %(name)-20s | %(message)s"

    def _create_logger_file(self):
        
        # check if the directory is present or not if present then override else create one
        os.makedirs(f'{self.BASE_DIR}/{self.Settings.LOGS_PATH}',exist_ok= True)

    def build_formatter(self):
        return logging.Formatter(self.log_format)


    def _add_console_handler(self,formatter):

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    def _add_file_handler(self,formatter):

        handler = logging.FileHandler(self.log_file)
        handler.setFormatter(formatter)
        return handler

    def get_logger(self):
        
        # 1. Create Logger File if not exist
        self._create_logger_file() 

        # 2. Create a get logger object by using the app name as classic_rag
        logger = logging.getLogger(self.logger_name)

        if not logger.handlers:

            # Create a Formatter object
            formatter = self.build_formatter()
            
            logger.addHandler(self._add_console_handler(formatter))
            logger.addHandler(self._add_file_handler(formatter))

            logger.setLevel(self.log_level)

        return logger


App_logger = Logger()
logger = App_logger.get_logger()