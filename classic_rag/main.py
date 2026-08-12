# from typing import List
# import uvicorn
# from fastapi import FastAPI
# from pydantic import BaseModel
# from generation.chain import RAGChain
# from config.logger import logger

# app = FastAPI(title="RAG API", description="FastAPI integrated with RAG Chain", version="1.0.0")
# chain = RAGChain()

# class Source(BaseModel):
#     page: int | str
#     type: str
#     source: str

# class queryRequest(BaseModel):
#     question : str

# class queryResponse(BaseModel):
#     answer: str
#     sources: List[Source]

# @app.get("/health")
# def health():
#         # raise HTTPException(status_code=404, detail="Card not found")
#     return {"staus": "ok"}


# @app.post("/query" , response_model= queryResponse)
# def query( request: queryRequest):

#     logger.info(f"Received query: {request.question}")
#     result = chain.invoke(request.question)
#     logger.info(result)
#     return queryResponse(
#         answer  = result["answer"],
#         sources = result["sources"]
#     )

# if __name__ == "__main__":
#     uvicorn.run("main:app",host="0.0.0.0", port=8002, reload=False)



from typing import List
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from generation.chain import RAGChain
from config.logger import logger


app = FastAPI(
    title="RAG API",
    description="FastAPI integrated with RAG Chain",
    version="1.0.0"
)

# Serve html, CSS, JS, images, etc.
app.mount("/frontend", StaticFiles(directory="Frontend"), name="frontend")
app.mount("/css",StaticFiles(directory="Frontend/css"),name="css")
app.mount("/js",StaticFiles(directory="Frontend/js"),name="js")


# =========================
# CORS CONFIGURATION
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# RAG CHAIN
# =========================

chain = RAGChain()


# =========================
# MODELS
# =========================

class Source(BaseModel):
    page: int | str
    type: str
    source: str


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]

# =========================
# UI
# =========================


@app.get("/")
async def serve_frontend():
    return FileResponse("Frontend/index.html")
    


# =========================
# HEALTH
# =========================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# =========================
# QUERY
# =========================

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):

    logger.info(f"Received query: {request.question}")

    result = chain.invoke(request.question)

    logger.info(result)

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"]
    )


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=False
    )