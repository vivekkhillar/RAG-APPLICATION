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



   ### PS C:\Users\Vivek\GIT Projects\RAG-APPLICATION> docker ps [check which container is up nd running]
   
   CONTAINER ID   IMAGE                  COMMAND                  CREATED       STATUS    <br>              PORTS                                             NAMES
   03a0c3ff6944   ollama/ollama:latest   "/bin/ollama serve"      6 weeks ago   Up 25 hours (healthy)   0.0.0.0:11434->11434/tcp, [::]<br>
   :11434->11434/tcp   banking_ollama<br>
   b7df87108373   postgres:16-alpine     "docker-entrypoint.s…"   6 weeks ago   Up 25 hours (healthy)   0.0.0.0:5433->5432/tcp, [::]<br>
   :5433->5432/tcp       banking_postgres<br><br>
   
   
   ### PS C:\Users\Vivek\GIT Projects\RAG-APPLICATION> docker exec -it banking_ollama ollama list<br> [which models are installed in ollama]
   NAME             ID              SIZE      MODIFIED   <br>
   llama3:latest    365c0bd3c000    4.7 GB    6 days ago    <br>

   What's next:<br>
      Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug banking_ollama<br>
      Learn more at https://docs.docker.com/go/debug-cli/<br>

   ### To pull any model from the ollama docker exec -it banking_ollama ollama pull llava
   
   PS C:\Users\Vivek\GIT Projects\RAG-APPLICATION> docker exec -it banking_ollama ollama list<br>
   NAME             ID              SIZE      MODIFIED<br>
   llama3:latest    365c0bd3c000    4.7 GB    6 days ago<br>

   What's next:<br>
      Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug banking_ollama<br>
      Learn more at https://docs.docker.com/go/debug-cli/<br>
   PS C:\Users\Vivek\GIT Projects\RAG-APPLICATION> docker exec -it banking_ollama ollama pull llava  <br>
   pulling manifest<br>
   pulling 170370233dd5: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████▏ 4.1 GB<br>
   pulling 72d6f08a42f6: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████▏ 624 MB<br>
   pulling 43070e2d4e53: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████▏  11 KB<br>
   pulling c43332387573: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████▏   67 B<br>
   pulling ed11eda7790d: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████▏   30 B<br>
   pulling 7c658f9561e5: 100% ▕██████████████████████████████████████████████████████████████████████████████████████████▏  564 B<br>
   verifying sha256 digest<br>
   writing manifest<br>
   success<br>

   What's next:<br>
      Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug banking_ollama<br>
      Learn more at https://docs.docker.com/go/debug-cli/<br>
