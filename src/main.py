from retriever import retrieve_similar_documents
from analyzer import generate_analysis
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class Party:
    def __init__(self):
        """Initialize the Party object."""
        pass
    
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


if __name__ == "__main__":
    # Simple test case
    liberal = Party()
    test_query = "what are your plans for growing population crisis"
    docs = liberal.retrieve(test_query)
    print(liberal.analyze(test_query, docs))
