from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import os

from agents.retriever import RetrieverAgent
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent

app = FastAPI(title="Multi-Agent RAG API", description="API for Multi-Agent RAG System using Ollama")

# Global instances (in a real system these would be more carefully scoped)
retriever = RetrieverAgent()
generator = GeneratorAgent()
reviewer = ReviewerAgent()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str
    is_hallucination: bool
    confidence: str
    sources: list

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document to the vector store."""
    try:
        content = await file.read()
        text = content.decode("utf-8")
        retriever.add_document(text, {"source": file.filename})
        return {"message": f"Successfully ingested {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def process_query(req: QueryRequest):
    """Run the Multi-Agent RAG pipeline."""
    try:
        # 1. Retrieve
        context_docs = retriever.retrieve(req.query)
        context_text = "\n\n".join([doc["text"] for doc in context_docs])
        sources = [doc["metadata"].get("source", "Unknown") for doc in context_docs]

        # 2. Generate
        draft_response = generator.generate(req.query, context_text)

        # 3. Review (Self-Correction)
        review_result = reviewer.review(req.query, draft_response, context_text)

        # If hallucination detected, generate again with stricter prompt or return a warning
        final_response = draft_response
        if review_result["is_hallucination"]:
            final_response = (
                "⚠️ **Self-Correction Alert**: The generated response may contain hallucinations "
                "or lack sufficient context. \n\n" + draft_response
            )

        return QueryResponse(
            query=req.query,
            response=final_response,
            is_hallucination=review_result["is_hallucination"],
            confidence=review_result["confidence"],
            sources=list(set(sources))
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
