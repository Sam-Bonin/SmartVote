# SmartVote: AI-Powered Policy Analysis Platform

SmartVote is an AI-powered web application that allows users to explore political party platforms. By leveraging semantic search and GPT-based analysis, the platform provides instant insights into complex policy documents, making them more accessible to voters.

## Features

- **Semantic Search**: Find specific policies and information across large party platform documents
- **AI Analysis**: Receive detailed explanations of party positions on various issues
- **PDF Integration**: View original source documents alongside AI analysis
- **Interactive UI**: User-friendly interface for exploring policy information
- **Efficient Caching**: In-memory caching of query embeddings and results for faster responses
- **Token Management**: Smart token limiting for optimal prompt generation

## Technical Overview

SmartVote integrates several advanced technologies:

- **Vector Embeddings**: Transforms text into vector representations for semantic search
- **Cosine Similarity**: Finds the most relevant policy sections for each query
- **GPT Models**: Generates clear, comprehensive analysis of policy positions
- **PDF Processing**: Extracts and processes text from official party documents
- **FastAPI Backend**: Provides efficient API endpoints for the frontend
- **Memory Optimization**: Stores only page references and embeddings in JSON, with lazy loading of text content
- **All data is stored in JSON files with no database dependencies**

## Requirements

- Python 3.9+
- OpenAI API key (for GPT-based analysis)
- Required packages (installed from requirements.txt):
  - FastAPI
  - Uvicorn
  - OpenAI
  - PyPDF
  - PyPDF2
  - Pydantic
  - python-dotenv
  - NumPy

## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/smartvote.git
   cd smartvote
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt  # requirements.txt is at the root level
   ```

4. Set up your OpenAI API key:
   ```
   # Create a .env file in the src directory
   cd src  # Navigate to the source code directory
   echo "OPENAI_API_KEY=your-api-key" > .env
   ```

5. Process the PDF and generate embeddings:
   ```
   # Run this script to process the Liberal.pdf file and create embeddings
   python data_processing.py
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
# Run this from the src directory
python data_processing.py
```

This will:
1. Process the PDF file in the data directory
2. Generate embeddings for each page
3. Save them to data/document_embeddings.json

## File Structure

- `app.py`: FastAPI application entry point with API endpoints
- `main.py`: Core functionality for the Party class
- `retriever.py`: Semantic search functions for document retrieval with caching
- `analyzer.py`: GPT-based analysis generation with token optimization
- `embedding.py`: Vector embedding utilities
- `data_processing.py`: PDF processing and reference management
- `cosine.py`: Optimized vector similarity calculations
- `config.py`: Centralized configuration for all hyperparameters
- `data/`: Directory containing the PDF documents and embeddings
- `index.html`: Main frontend interface
- `tests/`: Performance and API testing scripts

## How It Works

1. When first loaded, the application processes the PDF document and generates embeddings for each page
2. User enters a query about a policy area (e.g., "housing policy")
3. The query is converted to a vector embedding (cached for future use)
4. Vector similarity is used to find the most relevant sections of the party platform
5. Text content is loaded from the PDF only for the relevant pages
6. The relevant sections are sent to GPT with a token-optimized prompt
7. The analysis is returned to the user, along with links to the original document

## API Endpoints

- **POST /query**: Process a query and return analysis with relevant document sections
- **POST /clear-cache**: Clear the query and embedding caches
- **GET /health**: Simple endpoint to check if the service is running
- **GET /**: Serve the main application interface
- **GET /data/{file_path}**: Serve files from the data directory

## Performance Characteristics

Performance testing has identified the following characteristics:

| Component | Average Time (seconds) |
|-----------|------------------------|
| Query Embedding Generation | 0.68 |
| PDF Text Extraction (5 pages) | 0.63 |
| Loading Embeddings from JSON | 0.10 |
| Similarity Calculation | 0.06 |
| Analysis Generation (OpenAI API) | 5.29 |
| **End-to-End Query** | **6.76** |

### Real-World Performance

In real-world conditions with network delays and cold starts:

| Component | Time (seconds) |
|-----------|----------------|
| Cold Start Retrieval | 25-30 |
| API Processing | 5-7 |
| Network Delays | 2-3 |
| Frontend Rendering | 1-1.5 |
| **Total User Experience** | **33-41.5** |

### Key Bottlenecks

1. **Cold Start** (60-75% of real-world time): Initial document retrieval on first application load
2. **Analysis Generation** (76.6% of controlled test time): The OpenAI API call
3. **Query Embedding Generation** (46.2% of retrieval time): The embedding API call
4. **PDF Text Extraction** (42.8% of retrieval time): Extracting text from PDF pages

### Optimization Opportunities

The application implements several optimizations:
- In-memory caching of query embeddings and results
- Lazy loading of PDF text content
- Memory-efficient JSON structure storing only references
- Reduced document count (from 5 to 3) for analysis generation
- Token optimization for efficient prompts

Further optimizations implemented or planned:
- Cold start optimization with background warming
- Response caching for common queries
- Progressive UI loading for improved perceived performance
- Text content caching for frequently accessed PDF pages

See `tests/performance_analysis.md` for a detailed analysis and recommendations.

## Troubleshooting

- If you encounter issues starting the application, make sure you have activated the virtual environment:
  ```
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
- Ensure your OpenAI API key is properly set in the .env file in the src directory
- If you get module not found errors, verify that all dependencies are installed:
  ```
  pip install -r requirements.txt  # Run this from the root directory
  ```
- Check that the Liberal.pdf file exists in the src/data directory before running data_processing.py
- If you encounter errors about missing packages, try installing the specific missing package:
  ```
  pip install numpy  # Example for installing numpy if it's missing
  ```

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