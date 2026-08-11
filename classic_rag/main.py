from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from generation.chain import RAGChain
from config.logger import logger

app = FastAPI(title="RAG API", description="FastAPI integrated with RAG Chain", version="1.0.0")
chain = RAGChain()

class Source(BaseModel):
    page: int | str
    type: str
    source: str

class queryRequest(BaseModel):
    question : str

class queryResponse(BaseModel):
    answer: str
    sources: List[Source]

@app.get("/health")
def health():
        # raise HTTPException(status_code=404, detail="Card not found")
    return {"staus": "ok"}


@app.post("/query" , response_model= queryResponse)
def query( request: queryRequest):

    logger.info(f"Received query: {request.question}")
    result = chain.invoke(request.question)
    logger.info(result)
    return queryResponse(
        answer  = result["answer"],
        sources = result["sources"]
    )

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
