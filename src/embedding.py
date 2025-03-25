import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_embedding(text):
    """
    Get embedding vector for input text using OpenAI's embedding model.

    Args:
        text (str): Input text to get embedding for

    Returns:
        list: Embedding vector from OpenAI model, or None if an error occurs
    """
    # Input validation
    if not text or not isinstance(text, str):
        print("Error: Invalid input text for embedding")
        return None
        
    # Truncate extremely long texts to avoid token limits
    max_tokens = 8000  # Approximate limit for text-embedding-ada-002
    if len(text) > max_tokens * 4:  # Rough character to token ratio
        print(f"Warning: Truncating text from {len(text)} characters to ~{max_tokens} tokens")
        text = text[:max_tokens * 4]
    
    try:
        # Initialize OpenAI client with API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
            
        client = OpenAI(api_key=api_key)

        # Request embedding from OpenAI
        response = client.embeddings.create(
            model="text-embedding-ada-002", 
            input=text
        )

        # Return the embedding vector
        return response.data[0].embedding

    except Exception as e:
        print(f"Error getting embedding: {str(e)}")
        return None


if __name__ == "__main__":
    # Test the embedding function
    sample_text = "This is sample text for embedding"
    embedding = get_embedding(sample_text)
    
    if embedding:
        print(f"Generated embedding vector of length {len(embedding)} for sample text")
        print(f"First 5 values: {embedding[:5]}")
    else:
        print("Failed to generate embedding")
