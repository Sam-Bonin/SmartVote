from pypdf import PdfReader
import os
import json
from embedding import get_embedding
import PyPDF2
from config import MIN_TEXT_LENGTH


def process_pdf_and_create_embeddings(pdf_path, output_json_path=None, limit_pages=None):
    """
    Process a PDF file and create embeddings for each page
    
    Args:
        pdf_path (str): Path to the PDF file
        output_json_path (str, optional): Path to save the JSON output. Defaults to 'document_embeddings.json'.
        limit_pages (int, optional): Limit processing to first N pages. Defaults to None (all pages).
        
    Returns:
        list: List of dictionaries with page number and embeddings
    """
    if output_json_path is None:
        output_json_path = os.path.join("data", "document_embeddings.json")
        
    pdf_info_path = os.path.join("data", "pdf_info.json")
    
    # Check if PDF file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        # Save PDF path info to separate JSON file
        with open(pdf_info_path, 'w') as f:
            json.dump({"pdf_path": pdf_path}, f)
        
        embeddings_data = []
        
        # Open PDF file
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            
            # Limit pages if specified
            if limit_pages is not None:
                num_pages = min(num_pages, limit_pages)
                
            print(f"Processing {num_pages} pages from {pdf_path}")
            
            # Process each page
            for page_num in range(num_pages):
                try:
                    # Extract text from page
                    text = pdf_reader.pages[page_num].extract_text()
                    
                    # Skip pages with very little text
                    if len(text.strip()) < MIN_TEXT_LENGTH:
                        continue
                    
                    # Get embedding for the text
                    embedding = get_embedding(text)
                    if not embedding:
                        print(f"Warning: Failed to generate embedding for page {page_num + 1}, skipping.")
                        continue
                    
                    # Save only page reference and embedding, not full text
                    document_ref = {
                        "page_num": page_num + 1,  # 1-indexed for human readability
                        "file": pdf_path,
                        "embedding": embedding
                    }
                    
                    embeddings_data.append(document_ref)
                    print(f"Processed and stored embeddings for page {page_num + 1} of {num_pages}")
                except Exception as e:
                    print(f"Error processing page {page_num + 1}: {str(e)}")

        # Save all document references to JSON file
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        
        try:
            with open(output_json_path, "w") as f:
                json.dump(embeddings_data, f)
            print(f"Saved {len(embeddings_data)} document embeddings to {output_json_path}")
            
            return embeddings_data
        except Exception as e:
            print(f"Error saving embeddings to file: {str(e)}")
            return []
    except Exception as e:
        print(f"Error processing PDF file: {str(e)}")
        return []


def get_page_text(pdf_path, page_num):
    """
    Extract text from a specific page of a PDF file
    
    Args:
        pdf_path (str): Path to the PDF file
        page_num (int): Page number (1-indexed)
        
    Returns:
        str: Text content of the page
    """
    # Verify pdf_path is a string
    if not isinstance(pdf_path, str):
        raise TypeError("pdf_path must be a string")
        
    # Convert page_num to 0-indexed if it's 1-indexed
    page_index = page_num - 1 if page_num > 0 else page_num
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        # Open PDF file
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Check if page number is valid
            if page_index < 0 or page_index >= len(pdf_reader.pages):
                raise ValueError(f"Invalid page number: {page_num}. PDF has {len(pdf_reader.pages)} pages.")
            
            # Extract text from page
            text = pdf_reader.pages[page_index].extract_text()
            
            return text
    except Exception as e:
        print(f"Error extracting text from page {page_num}: {str(e)}")
        return ""


if __name__ == "__main__":
    try:
        pdf_path = os.path.join("data", "Liberal.pdf")
        embeddings_data = process_pdf_and_create_embeddings(pdf_path)
        print(f"Successfully created embeddings for {len(embeddings_data)} pages")
        print("Embeddings have been stored in the JSON file: data/document_embeddings.json")
    except Exception as e:
        print(f"Error: {str(e)}")
