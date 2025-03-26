import os
import json
import logging
import traceback
import uvicorn
from typing import Dict, Any, List
from config import API_HOST, API_PORT

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import Party

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware to allow requests from any origin (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get current directory and setup data path
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')

# Mount the data directory for serving PDFs
app.mount("/data", StaticFiles(directory=data_dir), name="data")

# Initialize the party object
party = Party()


# Define request and response models
class QueryInput(BaseModel):
    text: str


class ResponseItem(BaseModel):
    text: str
    score: float
    page: int


class QueryResponse(BaseModel):
    analysis: Dict[str, Any]
    similar_documents: List[ResponseItem]


class StatusResponse(BaseModel):
    status: str
    message: str


@app.post("/query")
async def query(query_input: QueryInput):
    """
    Process a query about the Liberal platform and return results.
    """
    try:
        # Log the incoming query
        logger.info(f"Received query: {query_input.text}")
        
        # Retrieve similar documents
        logger.info("Retrieving similar documents")
        similar_docs = party.retrieve(query_input.text)
        logger.info(f"Found {len(similar_docs)} similar documents")
        
        # Generate analysis
        logger.info("Generating analysis")
        analysis = party.analyze(query_input.text, similar_docs)
        logger.info("Analysis generation completed")
        
        # Transform page_num to page for frontend compatibility
        for doc in similar_docs:
            if 'page_num' in doc and 'page' not in doc:
                doc['page'] = doc['page_num']
                logger.debug(f"Using actual PDF page number: {doc['page']} (Note: Some PDF pages may have been skipped during embedding)")
            if 'similarity' in doc and 'score' not in doc:
                doc['score'] = doc['similarity']
        
        # Return the results
        return {
            "analysis": analysis,
            "similar_documents": similar_docs
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/query-stream")
async def query_stream(query_input: QueryInput):
    """
    Process a query with streaming response to display results as they become available.
    """
    async def generate():
        try:
            # Log the incoming query
            logger.info(f"Received streaming query: {query_input.text}")
            
            # Yield initial state with padding to ensure immediate display (browsers sometimes buffer small responses)
            padding = " " * 2048  # Add padding to force browser to start displaying
            yield json.dumps({"status": "processing", "step": "retrieval", "padding": padding}) + "\n"
            
            # Retrieve similar documents
            logger.info("Retrieving similar documents")
            similar_docs = party.retrieve(query_input.text)
            logger.info(f"Found {len(similar_docs)} similar documents")
            
            # Transform page_num to page for frontend compatibility
            for doc in similar_docs:
                if 'page_num' in doc and 'page' not in doc:
                    doc['page'] = doc['page_num']
                if 'similarity' in doc and 'score' not in doc:
                    doc['score'] = doc['similarity']
            
            # Send the documents immediately
            yield json.dumps({
                "status": "partial", 
                "step": "documents_ready",
                "similar_documents": similar_docs
            }) + "\n"
            
            # Generate analysis
            logger.info("Generating analysis")
            yield json.dumps({"status": "processing", "step": "analysis"}) + "\n"
            
            analysis = party.analyze(query_input.text, similar_docs)
            logger.info("Analysis generation completed")
            
            # Send the complete results
            yield json.dumps({
                "status": "complete",
                "analysis": analysis,
            }) + "\n"
            
        except Exception as e:
            logger.error(f"Error processing streaming query: {str(e)}")
            logger.error(traceback.format_exc())
            yield json.dumps({
                "status": "error",
                "message": str(e)
            }) + "\n"
    
    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering if used
            "Content-Encoding": "identity"  # Prevent compression which can cause buffering
        }
    )


@app.post("/clear-cache")
async def clear_cache():
    """
    Clear the query and embedding caches.
    """
    try:
        logger.info("Clearing query and embedding caches")
        result = party.clear_cache()
        return {"status": "success", "message": "Cache cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing cache: {str(e)}")


@app.get("/")
async def read_root():
    """Serve the index.html file."""
    try:
        with open(os.path.join(current_dir, "index.html"), "r") as file:
            return HTMLResponse(content=file.read())
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading index.html: {str(e)}")


@app.get("/data/{file_path:path}")
async def get_file(file_path: str):
    """
    Serve files from the data directory.
    This route is a fallback in case the StaticFiles mounting doesn't work.
    """
    try:
        file_path = os.path.join(data_dir, file_path)
        logger.info(f"Serving file: {file_path}")
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Special handling for PDF files to ensure proper content type
        if file_path.lower().endswith('.pdf'):
            return FileResponse(
                path=file_path,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": "inline; filename=" + os.path.basename(file_path),
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/pdf"
                }
            )
        
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error serving file {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "message": "Service is running"}


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
