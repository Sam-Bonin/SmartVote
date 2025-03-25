from pypdf import PdfReader
import os
import json
from embedding import get_embedding


def load_and_chunk_pdf(filename="Liberal.pdf"):
    """
    Process a PDF file, extract text from each page, generate embeddings, 
    and save to a JSON file.
    
    Args:
        filename (str): Name of the PDF file to process
        
    Returns:
        list: List of text chunks extracted from the PDF
    """
    # Construct path to PDF file in data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "data", filename)
    print(f"Attempting to read from: {pdf_path}")

    # Check if file exists before trying to read it
    if not os.path.exists(pdf_path):
        # Try alternate path in case data folder is at project root
        pdf_path = os.path.join(current_dir, "..", "data", filename)
        print(f"First path failed, trying: {pdf_path}")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"PDF file not found at either path. Please ensure {filename} exists in the data directory"
            )

    # Initialize PDF reader
    reader = PdfReader(pdf_path)
    
    # List to store all documents
    all_documents = []

    # Process each page
    for i, page in enumerate(reader.pages):
        # Extract text from page
        text = page.extract_text()
        
        # Skip pages with very little text
        if len(text.strip()) < 50:
            continue
        
        # Get embedding for the text
        embedding = get_embedding(text)
        
        # Save as document
        document = {
            "page": i + 1,  # 1-indexed for human readability
            "text": text,
            "embedding": embedding
        }
        
        all_documents.append(document)
        print(f"Processed and stored page {i + 1} of {len(reader.pages)}")

    # Save all documents to JSON file
    data_dir = os.path.join(current_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    embeddings_file = os.path.join(data_dir, "liberal_with_embeddings.json")
    
    with open(embeddings_file, "w") as f:
        json.dump(all_documents, f)
    
    print(f"Saved {len(all_documents)} documents with embeddings to {embeddings_file}")
    
    return [doc["text"] for doc in all_documents]


if __name__ == "__main__":
    try:
        chunks = load_and_chunk_pdf()
        print(f"Loaded and stored {len(chunks)} pages from PDF")
        print("Pages have been stored in the JSON file: data/liberal_with_embeddings.json")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the PDF file exists in the 'data' directory")
