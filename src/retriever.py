from embedding import get_embedding
from cosine import cosine_similarity
from data_processing import get_page_text, process_pdf_and_create_embeddings
import json
import os
from typing import Dict, List, Tuple, Optional
import numpy as np
from config import MAX_CACHE_SIZE, TOP_N_DOCUMENTS, SIMILARITY_THRESHOLD

# In-memory cache for query embeddings and results
query_embedding_cache = {}  # Cache for query embeddings
query_cache = {}  # Cache for query results

def get_cached_embedding(query):
    """Get embedding for a query, using cache if available"""
    if query in query_embedding_cache:
        return query_embedding_cache[query]
    
    # Generate and cache embedding
    embedding = get_embedding(query)
    if len(query_embedding_cache) >= MAX_CACHE_SIZE:
        # Simple cache eviction - remove oldest item
        query_embedding_cache.pop(next(iter(query_embedding_cache)))
    
    query_embedding_cache[query] = embedding
    return embedding

def clear_cache():
    """Clear all caches"""
    global query_embedding_cache, query_cache
    query_embedding_cache.clear()
    query_cache.clear()
    print("Query cache cleared")

def retrieve_similar_documents(query, top_n=TOP_N_DOCUMENTS):
    """
    Retrieve documents similar to the query using vector similarity.
    
    Args:
        query (str): The user query
        top_n (int): Number of top results to return
        
    Returns:
        list: List of dictionaries containing similar documents
    """
    # Check query cache first
    if query in query_cache:
        print(f"Cache hit! Using cached results for query: {query}")
        return query_cache[query]
    
    # Get query embedding (check cache first)
    query_embedding = get_cached_embedding(query)
    
    # Load document embeddings from file or create if it doesn't exist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    embeddings_file = os.path.join(data_dir, "document_embeddings.json")
    pdf_info_file = os.path.join(data_dir, "pdf_info.json")
    
    # Default PDF path
    pdf_path = os.path.join(data_dir, "Liberal.pdf")
    
    if not os.path.exists(embeddings_file) or os.path.getsize(embeddings_file) == 0:
        print("Embeddings file not found, generating embeddings...")
        
        # Check if PDF info exists, default to Liberal.pdf
        if os.path.exists(pdf_info_file):
            with open(pdf_info_file, 'r') as f:
                pdf_info = json.load(f)
                pdf_path = pdf_info.get("pdf_path", os.path.join(data_dir, "Liberal.pdf"))
        else:
            pdf_path = os.path.join(data_dir, "Liberal.pdf")
            
        process_pdf_and_create_embeddings(pdf_path)
    
    # Load embeddings data
    try:
        with open(embeddings_file, "r") as f:
            document_embeddings = json.load(f)
    except Exception as e:
        print(f"Error loading embeddings: {str(e)}")
        document_embeddings = []
        
    # Also load PDF info
    try:
        with open(pdf_info_file, 'r') as f:
            pdf_info = json.load(f)
            pdf_path = pdf_info.get("pdf_path", os.path.join(data_dir, "Liberal.pdf"))
    except Exception as e:
        print(f"Error loading PDF info: {str(e)}")
        pdf_path = os.path.join(data_dir, "Liberal.pdf")
    
    # Calculate similarity scores
    results = []
    for doc_ref in document_embeddings:
        doc_embedding = doc_ref["embedding"]
        
        # Calculate cosine similarity
        similarity = np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
        )
        
        # Only include if similarity is above threshold
        if similarity > SIMILARITY_THRESHOLD:
            page_num = doc_ref["page_num"]
            file = doc_ref.get("file", "Liberal.pdf")
            
            # Use full path for PDF if just filename is stored
            pdf_file_path = file if os.path.exists(file) else pdf_path
            
            # Get text content directly from PDF
            text = get_page_text(pdf_file_path, page_num)
            
            results.append({
                "page_num": page_num,
                "page": page_num,  # Add page field for frontend compatibility
                "similarity": float(similarity),  # Convert numpy float to native Python float
                "score": float(similarity),  # Add score field for frontend compatibility
                "text": text,
            })
    
    # Sort by similarity (highest first)
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Limit to top_n results
    top_results = results[:top_n]
    
    # Cache the results if we have space
    if len(query_cache) >= MAX_CACHE_SIZE:
        # Simple cache eviction - remove oldest item
        query_cache.pop(next(iter(query_cache)))
    
    query_cache[query] = top_results
    
    return top_results

if __name__ == "__main__":
    # Test retrieval
    query = "Housing crisis"
    results = retrieve_similar_documents(query, top_n=TOP_N_DOCUMENTS)
    
    print(f"\nResults for query: '{query}'")
    for i, result in enumerate(results):
        print(f"\n{i+1}. Page {result['page_num']} (Similarity: {result['similarity']:.4f})")
        print(f"Text snippet: {result['text'][:100]}...")
        
    # Test caching
    print("\nRunning query again (should use cache):")
    results = retrieve_similar_documents(query, top_n=TOP_N_DOCUMENTS)
    
    # Test with a different query
    query2 = "Climate change"
    results2 = retrieve_similar_documents(query2, top_n=TOP_N_DOCUMENTS)
    
    print(f"\nResults for query: '{query2}'")
    for i, result in enumerate(results2):
        print(f"\n{i+1}. Page {result['page_num']} (Similarity: {result['similarity']:.4f})")
        print(f"Text snippet: {result['text'][:100]}...")
