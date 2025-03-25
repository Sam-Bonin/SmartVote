from embedding import get_embedding
from cosine import cosine_similarity
from data_processing import get_page_text, process_pdf_and_create_embeddings
import json
import os
from typing import Dict, List, Tuple, Optional

# Simple in-memory cache for query embeddings
query_embedding_cache: Dict[str, List[float]] = {}
# Simple in-memory cache for query results
query_results_cache: Dict[str, List[Dict]] = {}

# Maximum cache size
MAX_CACHE_SIZE = 100


def retrieve_similar_documents(query: str, top_n: int = 25) -> List[Dict]:
    """
    Retrieve documents from the Liberal Party platform that are similar to the query.
    
    Args:
        query (str): The search query
        top_n (int, optional): Number of similar documents to return. Defaults to 25.
        
    Returns:
        list: List of dictionaries containing text, score, and page number
    """
    # Check if results are in cache
    if query in query_results_cache:
        print(f"Cache hit! Using cached results for query: {query}")
        return query_results_cache[query][:top_n]
    
    # Get query embedding (check cache first)
    if query in query_embedding_cache:
        print(f"Using cached embedding for query: {query}")
        query_embedding = query_embedding_cache[query]
    else:
        query_embedding = get_embedding(query)
        # Add to cache (with simple eviction strategy if cache is full)
        if len(query_embedding_cache) >= MAX_CACHE_SIZE:
            # Remove a random item (could be improved with LRU strategy)
            query_embedding_cache.pop(next(iter(query_embedding_cache)))
        query_embedding_cache[query] = query_embedding
    
    # Check if embeddings file exists, if not create it
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")
    embeddings_file = os.path.join(data_dir, "document_embeddings.json")
    
    if not os.path.exists(embeddings_file):
        print("Embeddings file not found. Generating embeddings...")
        num_pages = process_pdf_and_create_embeddings()
        if num_pages == 0:
            raise Exception("Failed to generate embeddings")
    
    # Load document embeddings
    try:
        with open(embeddings_file, "r") as f:
            document_refs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise Exception(f"Error loading embeddings: {str(e)}")
    
    # Calculate similarity scores
    similarity_scores = []
    for doc_ref in document_refs:
        doc_embedding = doc_ref["embedding"]
        score = cosine_similarity(query_embedding, doc_embedding)
        similarity_scores.append((doc_ref, score))
    
    # Sort by similarity score (descending)
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get top N results
    top_results = similarity_scores[:top_n]
    
    # Load the actual text for only the top results
    results = []
    for doc_ref, score in top_results:
        page_num = doc_ref["page_num"]
        file = doc_ref.get("file", "Liberal.pdf")
        
        # Get text content directly from PDF
        text = get_page_text(page_num, file)
        
        results.append({
            "text": text,
            "score": score,
            "page": page_num
        })
    
    # Cache the results
    if len(query_results_cache) >= MAX_CACHE_SIZE:
        # Simple eviction strategy
        query_results_cache.pop(next(iter(query_results_cache)))
    query_results_cache[query] = results
    
    return results


def clear_cache():
    """Clear the query cache"""
    global query_embedding_cache, query_results_cache
    query_embedding_cache.clear()
    query_results_cache.clear()
    print("Query cache cleared")


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
    
    # Test caching
    print("\nRunning same query again to test caching...")
    results2 = retrieve_similar_documents(sample_query, top_n=5)
    print(f"Returned {len(results2)} results from cache")
