import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any, List
from main import Party
import uvicorn
import json

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

# Mount the data directory for serving PDFs
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')
app.mount("/data", StaticFiles(directory=data_dir), name="data")

# Initialize the party object (assuming Party is defined in main.py)
party = Party()

class QueryInput(BaseModel):
    text: str

class ResponseItem(BaseModel):
    text: str
    score: float
    page: int

class QueryResponse(BaseModel):
    analysis: Dict[str, Any]
    similar_documents: List[ResponseItem]


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
        
        # Return the results
        return {
            "analysis": analysis,
            "similar_documents": similar_docs
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/")
async def read_root():
    """
    Serve the index.html file.
    """
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


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
