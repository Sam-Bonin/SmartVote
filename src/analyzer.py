from openai import OpenAI

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
        
        # Prepare context from documents (use top 10 docs for context)
        context = ""
        max_docs = min(10, len(documents))
        for i, doc in enumerate(documents[:max_docs]):
            context += f"\nDocument {i+1} (Page {doc['page']}):\n{doc['text']}\n"
        
        # Create the prompt for analysis
        prompt = f"""
You are an expert political analyst specializing in Canadian Liberal Party policies.
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
            max_tokens=600
        )
        
        return {"response": response.choices[0].message.content}
    
    except Exception as e:
        # Return error message if analysis generation fails
        return {"response": f"An error occurred while generating the analysis: {str(e)}"}

if __name__ == "__main__":
    # Test the analyzer with a sample query and document
    sample_query = "What is the Liberal Party's position on climate change?"
    sample_doc = [{
        "text": "The Liberal Party is committed to fighting climate change through carbon pricing, clean energy investments, and achieving net-zero emissions by 2050.",
        "score": 0.95,
        "page": 42
    }]
    
    analysis = generate_analysis(sample_query, sample_doc)
    print(analysis["response"]) 