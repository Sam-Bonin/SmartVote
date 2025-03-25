from pypdf import PdfReader
import os
import json
from embedding import get_embedding


def process_pdf_and_create_embeddings(filename="Liberal.pdf"):
    """
    Process a PDF file, extract text from each page, generate embeddings, 
    and save embeddings and page references to a JSON file.
    
    Args:
        filename (str): Name of the PDF file to process
        
    Returns:
        int: Number of pages processed
    """
    # Construct path to PDF file in data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    pdf_path = os.path.join(data_dir, filename)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}. Please ensure {filename} exists in the data directory.")

    # Initialize PDF reader
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")
    
    # List to store document references and embeddings
    document_embeddings = []

    # Process each page
    for i, page in enumerate(reader.pages):
        try:
            # Extract text from page
            text = page.extract_text()
            
            # Skip pages with very little text
            if len(text.strip()) < 50:
                continue
            
            # Get embedding for the text
            embedding = get_embedding(text)
            if not embedding:
                print(f"Warning: Failed to generate embedding for page {i + 1}, skipping.")
                continue
            
            # Save only page reference and embedding, not full text
            document_ref = {
                "page_num": i + 1,  # 1-indexed for human readability
                "file": filename,
                "embedding": embedding
            }
            
            document_embeddings.append(document_ref)
            print(f"Processed and stored embeddings for page {i + 1} of {len(reader.pages)}")
        except Exception as e:
            print(f"Error processing page {i + 1}: {str(e)}")

    # Save all document references to JSON file
    os.makedirs(data_dir, exist_ok=True)
    embeddings_file = os.path.join(data_dir, "document_embeddings.json")
    
    try:
        with open(embeddings_file, "w") as f:
            json.dump(document_embeddings, f)
        print(f"Saved {len(document_embeddings)} document embeddings to {embeddings_file}")
        
        # Save the path to the PDF for later retrieval
        pdf_info_file = os.path.join(data_dir, "pdf_info.json")
        with open(pdf_info_file, "w") as f:
            json.dump({"pdf_path": pdf_path}, f)
        
        return len(document_embeddings)
    except Exception as e:
        print(f"Error saving embeddings to file: {str(e)}")
        return 0


def get_page_text(page_num, filename="Liberal.pdf"):
    """
    Extract text from a specific page of the PDF.
    
    Args:
        page_num (int): The page number to extract (1-indexed)
        filename (str): Name of the PDF file
        
    Returns:
        str: The extracted text from the page
    """
    # Construct path to PDF file in data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    pdf_path = os.path.join(data_dir, filename)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    try:
        # Initialize PDF reader
        reader = PdfReader(pdf_path)
        
        # Adjust page number to 0-indexed
        page_idx = page_num - 1
        
        # Check if page exists
        if page_idx < 0 or page_idx >= len(reader.pages):
            raise ValueError(f"Page {page_num} out of range (total pages: {len(reader.pages)})")
        
        # Extract and return text
        return reader.pages[page_idx].extract_text()
    except Exception as e:
        print(f"Error extracting text from page {page_num}: {str(e)}")
        return ""


if __name__ == "__main__":
    try:
        num_pages = process_pdf_and_create_embeddings()
        print(f"Successfully created embeddings for {num_pages} pages")
        print("Embeddings have been stored in the JSON file: data/document_embeddings.json")
        
        # Test the page text extraction
        sample_page = 5
        text = get_page_text(sample_page)
        print(f"\nSample text from page {sample_page}:")
        print(text[:200] + "..." if len(text) > 200 else text)
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure the PDF file exists in the 'data' directory")
