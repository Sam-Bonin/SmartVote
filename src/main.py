from retriever import retrieve_similar_documents, clear_cache
from analyzer import generate_analysis
import json
from dotenv import load_dotenv

load_dotenv()


class Party:
    def __init__(self):
        """Initialize the Party object."""
        self._cache_enabled = True
    
    def retrieve(self, query):
        """
        Retrieve similar documents based on the query.
        
        Args:
            query (str): The query to search for.
            
        Returns:
            list: A list of similar documents.
        """
        return retrieve_similar_documents(query)
    
    def analyze(self, query, similar_docs):
        """
        Generate analysis based on the query and similar documents.
        
        Args:
            query (str): The query to analyze.
            similar_docs (list): A list of similar documents.
            
        Returns:
            dict: The analysis result.
        """
        return generate_analysis(query, similar_docs)
    
    def clear_cache(self):
        """
        Clear the query and embedding cache.
        """
        clear_cache()
        return {"status": "Cache cleared successfully"}


if __name__ == "__main__":
    # Simple test case
    liberal = Party()
    
    # First query
    test_query = "what are your plans for growing population crisis"
    print(f"Query: '{test_query}'")
    docs = liberal.retrieve(test_query)
    print(f"Found {len(docs)} relevant documents")
    analysis = liberal.analyze(test_query, docs)
    print("\nAnalysis:")
    print(analysis["response"][:300] + "..." if len(analysis["response"]) > 300 else analysis["response"])
    
    # Second query (same) to test caching
    print("\nRepeating the same query to test caching:")
    docs2 = liberal.retrieve(test_query)
    print(f"Found {len(docs2)} relevant documents (from cache)")
    
    # Clear cache
    print("\nClearing cache...")
    liberal.clear_cache()
    
    # New query
    new_query = "What is your healthcare policy?"
    print(f"\nNew query: '{new_query}'")
    docs3 = liberal.retrieve(new_query)
    print(f"Found {len(docs3)} relevant documents")
