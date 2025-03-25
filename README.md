# SmartVote: AI-Powered Policy Analysis Platform

SmartVote is an AI-powered web application that allows users to explore political party platforms. By leveraging semantic search and GPT-based analysis, the platform provides instant insights into complex policy documents, making them more accessible to voters.

## Features

- **Semantic Search**: Find specific policies and information across large party platform documents
- **AI Analysis**: Receive detailed explanations of party positions on various issues
- **PDF Integration**: View original source documents alongside AI analysis
- **Interactive UI**: User-friendly interface for exploring policy information

## Technical Overview

SmartVote integrates several advanced technologies:

- **Vector Embeddings**: Transforms text into vector representations for semantic search
- **Cosine Similarity**: Finds the most relevant policy sections for each query
- **GPT Models**: Generates clear, comprehensive analysis of policy positions
- **PDF Processing**: Extracts and processes text from official party documents
- **FastAPI Backend**: Provides efficient API endpoints for the frontend
- **All data is stored in JSON files with no database dependencies**

## Requirements

- Python 3.9+
- FastAPI
- OpenAI API key
- PyPDF2 for PDF processing
- Pydantic for data validation

## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/username/smartvote.git
   cd smartvote
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```
   # Create a .env file in the project root
   echo "OPENAI_API_KEY=your-api-key" > .env
   ```

5. Process the PDF and generate embeddings:
   ```
   # Run this script to process the Liberal.pdf file and create embeddings
   python -m data_processing
   ```

6. Start the application:
   ```
   python app.py
   ```

7. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Manually Generating Embeddings

If the app doesn't automatically generate embeddings on first run, you can manually trigger the process:

```python
# Run this from the smartvote directory
python -c "from retriever import save_embeddings_to_file; save_embeddings_to_file()"
```

This will:
1. Process the PDF file in the data directory
2. Generate embeddings for each page
3. Save them to data/liberal_with_embeddings.json

## File Structure

- `app.py`: FastAPI application entry point
- `main.py`: Core functionality for the Party class
- `retriever.py`: Semantic search functions for document retrieval
- `analyzer.py`: GPT-based analysis generation
- `embedding.py`: Vector embedding utilities
- `data_processing.py`: PDF processing and JSON storage functions
- `data/`: Directory containing the PDF documents and embeddings
- `index.html`: Main frontend interface

## How It Works

1. When first loaded, the application processes the PDF document and generates embeddings for each page
2. User enters a query about a policy area (e.g., "housing policy")
3. The query is converted to a vector embedding
4. Vector similarity is used to find the most relevant sections of the party platform
5. The relevant sections are sent to GPT with a prompt to analyze the party's position
6. The analysis is returned to the user, along with links to the original document

## Future Development

- Add support for multiple party platforms
- Implement caching for common queries
- Add user accounts and saved searches
- Expand to include historical platform comparisons
- Integrate with election data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 