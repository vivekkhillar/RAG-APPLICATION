## What is resolve() function do in the Python 
   
   From pathlib import path  <br>
   base_dir = Path(__file__).resolve()<br> 
   Which will return the full absolute path access. you can append the .resolve().parent.parent to access the parent location

## BaseSettings and SettingsConfigDict work together: one defines your settings, the other defines how to load them.

   BaseSettings — the settings loader

   Think of it as a smart form that fills itself from config files or environment variables.

   #### You define what you need:

   OLLAMA_URL: str<br>
   CHUNK_SIZE: int<br>
   
   <b>When you write Settings(), </b> 
   
   Reads values from .env (and OS env vars) Puts them into those fields, Checks types ("400" → 400 for int) and
   Errors if something is missing or wrong
   Without BaseSettings, you’d do this manually:

   import os<br>
   OLLAMA_URL = os.getenv("OLLAMA_URL")  # easy to forget, no type check<br>
   With BaseSettings, you get one typed<br>
   object: settings.OLLAMA_URL, settings.CHUNK_SIZE.

   <b>SettingsConfigDict — the instructions </b>
   This is a settings dictionary that tells BaseSettings how to load data.

   In your code:

   model_config = SettingsConfigDict(<br>
      env_file=ENV_FILE,<br>
      env_file_encoding="utf-8"<br>
   )<br>

   In plain terms:

   Option	What it means
   env_file=ENV_FILE “Read config from this .env file”<br>
   env_file_encoding="utf-8" “Read the file as normal text (UTF-8)”<br>
   model_config is just the name Pydantic expects for these instructions on the class.

   How they work together

   SettingsConfigDict  →  "Read classic_rag/.env"<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+<br>
   BaseSettings        →  "I need OLLAMA_URL, CHUNK_SIZE, ..."<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
   Settings()            →  settings object with all values filled<br>
   SettingsConfigDict = where to read from<br>
   BaseSettings = what to read and how to validate it<br>
   One-line summary<br>
   BaseSettings — turns env/config into a Python object with typed fields<br>
   SettingsConfigDict — tells it which .env file to use and how to read it<br>