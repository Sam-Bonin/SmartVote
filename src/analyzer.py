from openai import OpenAI
import re
import math

# Constants for token limits
MAX_TOKENS_TOTAL = 4000  # Maximum tokens for the model's context
MAX_TOKENS_OUTPUT = 600  # Maximum tokens for the output
MAX_TOKENS_PROMPT = MAX_TOKENS_TOTAL - MAX_TOKENS_OUTPUT  # Reserve space for output

# Approximate token count for system message
SYSTEM_MESSAGE_TOKENS = 100

# Rough estimate: 1 token is about 4 characters in English text
CHARS_PER_TOKEN = 4 


def estimate_token_count(text):
    """
    Estimate the number of tokens in a text string.
    This is a rough approximation based on character count.
    
    Args:
        text (str): The text to estimate tokens for
        
    Returns:
        int: Estimated number of tokens
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Estimate tokens based on character count
    return max(1, math.ceil(len(text) / CHARS_PER_TOKEN))


def truncate_context(documents, max_tokens):
    """
    Truncate the document context to fit within token limits.
    
    Args:
        documents (list): List of document dictionaries
        max_tokens (int): Maximum tokens allowed for context
        
    Returns:
        str: Truncated context string
    """
    context = ""
    current_tokens = 0
    used_documents = 0
    
    for i, doc in enumerate(documents):
        # Format document text
        doc_text = f"\nDocument {i+1} (Page {doc['page']}):\n{doc['text']}\n"
        
        # Estimate tokens for this document
        doc_tokens = estimate_token_count(doc_text)
        
        # Check if adding this document would exceed the limit
        if current_tokens + doc_tokens > max_tokens:
            # If we haven't used any documents yet but the first one is too big,
            # truncate it to fit
            if used_documents == 0:
                # Calculate how many characters we can include
                max_chars = max_tokens * CHARS_PER_TOKEN
                truncated_text = doc['text'][:max_chars] + "..."
                context = f"\nDocument 1 (Page {doc['page']}):\n{truncated_text}\n"
                used_documents = 1
            break
        
        # Add this document to the context
        context += doc_text
        current_tokens += doc_tokens
        used_documents += 1
    
    print(f"Using {used_documents} of {len(documents)} documents in context (estimated {current_tokens} tokens)")
    return context


def generate_analysis(query, documents):
    """
    Generate an analysis of the Liberal Platform based on the query and retrieved documents.
    
    Args:
        query (str): The user's query
        documents (list): List of retrieved documents
        
    Returns:
        dict: Analysis response containing the generated text
    """
    # Check input validity
    if not query or not documents:
        return {"response": "Invalid query or no relevant documents found."}
    
    try:
        # Create OpenAI client
        client = OpenAI()
        
        # Calculate token budget for context
        query_tokens = estimate_token_count(query)
        prompt_template_tokens = 200  # Approximate tokens for the prompt template
        available_context_tokens = MAX_TOKENS_PROMPT - SYSTEM_MESSAGE_TOKENS - query_tokens - prompt_template_tokens
        
        # Prepare context from documents with token limiting
        context = truncate_context(documents, available_context_tokens)
        
        # Create the prompt for analysis
        prompt = f"""
Analyze the following query about the Liberal Party platform: "{query}"

I'll provide context from the Liberal Party platform document. Use ONLY this information to formulate your response.

Context from Liberal Party Platform:
{context}

Generate a comprehensive analysis that:
1. Directly answers the query
2. Highlights key policy points relevant to the question
3. Provides specific details from the platform
4. Uses a neutral, informative tone
5. Uses markdown formatting with **bold** for important points
6. Is concise but thorough (250-350 words)

Your response:
"""
        
        # Generate completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert political analyst specializing in Canadian Liberal Party policies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=MAX_TOKENS_OUTPUT
        )
        
        return {"response": response.choices[0].message.content}
    
    except Exception as e:
        # Return error message if analysis generation fails
        return {"response": f"An error occurred while generating the analysis: {str(e)}"}


if __name__ == "__main__":
    # Test the analyzer with a sample query and document
    sample_query = "What is the Liberal Party's position on climate change?"
    sample_docs = [
        {
            "text": "The Liberal Party is committed to fighting climate change through carbon pricing, clean energy investments, and achieving net-zero emissions by 2050. Our plan includes investing in renewable energy infrastructure, phasing out coal power plants, and incentivizing electric vehicle adoption through rebates and expanding charging networks across the country.",
            "score": 0.95,
            "page": 42
        },
        {
            "text": "The Liberal climate plan will ensure that pollution is no longer free. We will continue to put a price on carbon while returning money to Canadian families through rebates. This market-based approach is both effective at reducing emissions and economically sound.",
            "score": 0.92,
            "page": 43
        }
    ]
    
    analysis = generate_analysis(sample_query, sample_docs)
    print("\nGenerated Analysis:")
    print(analysis["response"])
    
    # Test token estimation
    test_text = "This is a test string for token estimation."
    print(f"\nEstimated tokens for test text: {estimate_token_count(test_text)}") 