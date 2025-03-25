from embedding import get_embedding
from cosine import cosine_similarity
import json
import os


def retrieve_similar_documents(query, top_n=25):
    """
    Retrieve documents from the Liberal Party platform that are similar to the query.
    
    Args:
        query (str): The search query
        top_n (int, optional): Number of similar documents to return. Defaults to 25.
        
    Returns:
        list: List of dictionaries containing text, score, and page number
    """
    # Get query embedding
    query_embedding = get_embedding(query)
    
    # Check if embeddings file exists, if not create it
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    embeddings_file = os.path.join(data_dir, "liberal_with_embeddings.json")
    
    if not os.path.exists(embeddings_file):
        save_embeddings_to_file()
    
    # Load documents and their embeddings
    try:
        with open(embeddings_file, "r") as f:
            documents = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to create embeddings again
        save_embeddings_to_file()
        with open(embeddings_file, "r") as f:
            documents = json.load(f)
    
    # Calculate similarity scores
    results = []
    for doc in documents:
        doc_embedding = doc["embedding"]
        score = cosine_similarity(query_embedding, doc_embedding)
        results.append({
            "text": doc["text"],
            "score": score,
            "page": doc["page"]
        })
    
    # Sort by similarity score (descending)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top N results
    return results[:top_n]


def save_embeddings_to_file():
    """
    Extract data from PDF and save embeddings to a JSON file.
    """
    import PyPDF2
    
    # Get file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    pdf_path = os.path.join(data_dir, "Liberal.pdf")
    
    # Open PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # List to store all documents
        all_documents = []
        
        # Process each page
        for page_num in range(len(pdf_reader.pages)):
            # Extract text from page
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            # Skip pages with very little text
            if len(text.strip()) < 50:
                continue
            
            # Get embedding for the text
            embedding = get_embedding(text)
            
            # Save as document
            document = {
                "page": page_num + 1,  # 1-indexed for human readability
                "text": text,
                "embedding": embedding
            }
            
            all_documents.append(document)
            print(f"Processed and stored page {page_num + 1} of {len(pdf_reader.pages)}")
    
    # Save all documents to JSON file
    embeddings_file = os.path.join(data_dir, "liberal_with_embeddings.json")
    with open(embeddings_file, "w") as f:
        json.dump(all_documents, f)
    
    print(f"Saved {len(all_documents)} documents with embeddings to {embeddings_file}")


if __name__ == "__main__":
    # Test query
    sample_query = "Housing crisis"

    # Get similar documents
    results = retrieve_similar_documents(sample_query, top_n=5)

    # Print results
    print(f"\nTop results for query: '{sample_query}'\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i}")
        print(f"Page: {result['page']}")
        print(f"Similarity Score: {result['score']:.4f}")
        print(f"Text snippet: {result['text'][:150]}...")  # Show first 150 chars
        print()
