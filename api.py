"""
FastAPI Backend Server for RAG Query System
Provides REST API endpoints for the React frontend
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query_handler import QueryHandler
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Gojira Album Chat API",
    description="RAG-based query system for Gojira albums",
    version="1.0.0"
)

# Configure CORS - allow React frontend to connect
# Support environment variable for production frontend URL
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize query handler (singleton - initialized once)
# Using llama3.2:3b (~2GB) - fits in available memory after system overhead
handler = QueryHandler(llm_model="llama3.2:3b")


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    k: int = 10  # Number of documents to retrieve


class QueryResponse(BaseModel):
    answer: str
    query: str
    routing: dict = None


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Gojira Album Chat API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Main query endpoint
@app.post("/api/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process a query and return the answer with routing information
    """
    try:
        # Get routing info first (without verbose output)
        routing = handler.router.route_query(request.query)
        
        # Execute query (verbose=False for API responses)
        answer_text = handler.query(
            request.query, 
            k=request.k, 
            verbose=False
        )
        
        return QueryResponse(
            answer=answer_text,
            query=request.query,
            routing={
                "query_type": routing.get("query_type"),
                "sections": routing.get("sections", []),
                "albums": routing.get("albums", []),
                "confidence": routing.get("confidence", 0),
                "method": routing.get("method", "unknown")
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


# Run the server
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )

