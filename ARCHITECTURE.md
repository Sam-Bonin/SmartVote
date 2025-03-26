# SmartVote Architecture and Flow Diagrams

This document provides a detailed explanation of the SmartVote application architecture, including flow diagrams for both the pre-computing phase and the live query phase.

## System Components

SmartVote consists of several key components that work together:

1. **Web Interface** (`index.html`): The frontend that users interact with
2. **API Server** (`app.py`): FastAPI application serving requests
3. **Core Logic** (`main.py`): Contains the Party class with main functionality
4. **Retriever** (`retriever.py`): Handles semantic document retrieval with caching
5. **Analyzer** (`analyzer.py`): Generates policy analysis using OpenAI with token optimization
6. **Embedding Utility** (`embedding.py`): Creates vector embeddings
7. **Data Processor** (`data_processing.py`): Processes PDF documents and saves references
8. **Vector Math** (`cosine.py`): Provides optimized similarity calculations

## Application Flow

The SmartVote application operates in two distinct phases:

### Phase 1: Pre-computing (PDF Processing and Embedding Generation)

This phase happens before the application serves user queries. It involves processing the PDF document and generating embeddings.

```
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Vector     │────>│ Store Data    │────>│ JSON File  │ 
│  Embeddings │     │ References    │     │ (document_ │ 
└─────────────┘     └─────────────┘       │ embeddings.json)│ 
                                          └────────────┘ 
```

**Detailed Flow:**

1. The process begins with `data_processing.py`
2. The PDF file (`Liberal.pdf`) is loaded using PyPDF2
3. Text is extracted from each page
4. For each page:
   - The text is processed to remove unwanted characters
   - The text is sent to OpenAI's embedding API through `embedding.py`
   - The returned vector embedding is paired with the page reference (not full text)
5. The references and embeddings are stored in a JSON file (`document_embeddings.json`)

**Code Flow:**

1. `data_processing.py` (function: `process_pdf_and_create_embeddings()`):
   - Opens the PDF file and creates a PDF reader
   - Loops through each page
   - Extracts text from each page
   - Gets embedding for the text via `embedding.py`
   - Creates a document reference with page number and embedding (not full text)
   - Adds the document reference to a list
   - Saves the list to a JSON file
   - Provides `get_page_text()` function to retrieve text when needed

### Phase 2: Live Query Processing

This phase happens when a user submits a query through the web interface.

```
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  User       │────>│ Web Interface │────>│ User enters│────>│ index.html     │
│  Browser    │     │ (index.html)  │     │ query      │     │ JavaScript     │
└─────────────┘     └───────────────┘     └────────────┘     └────────┬───────┘
                                                                      │
                                                                      ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  FastAPI    │<────│ /query        │<────│ AJAX Post  │<────│ Fetch API      │
│  (app.py)   │     │ endpoint      │     │ Request    │     │ Request        │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────────────┘
       │
       ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Party class│────>│ main.py       │────>│ Process    │────>│ 1. retrieve()  │
│             │     │               │     │ Query      │     │ 2. analyze()   │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  retriever  │────>│ Check Query   │────>│ Return     │────>│ Query Cache    │
│  .py        │     │ Cache         │     │ Cached     │     │                │
└──────┬──────┘     └───────────────┘     │ Results    │     └────────────────┘
       │                                   └────────────┘
       ▼                                            
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Get Query  │────>│ Check         │────>│ Return     │────>│ Embedding Cache│
│  Embedding  │     │ Embedding     │     │ Cached     │     │                │
└──────┬──────┘     │ Cache         │     │ Embedding  │     └────────────────┘
       │            └───────────────┘     └────────────┘
       ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Load JSON  │────>│ Compare with  │────>│ Rank by    │────>│ Return Top     │
│  Embeddings │     │ Stored Vectors│     │ Similarity │     │ Documents      │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Load Text  │────>│ From PDF File │────>│ Only for   │────>│ Top Results    │
│  Content    │     │               │     │ Top Results│     │                │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  analyzer.py│────>│ Token Count   │────>│ Truncate   │────>│ Optimize       │
│             │     │ Estimation    │     │ Context    │     │ Prompt Length  │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Generate   │────>│ OpenAI API    │────>│ GPT-4o mini│────>│ Analysis       │
│  Analysis   │     │ (Chat)        │     │ Model      │     │ Response       │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Response   │────>│ JSON Data     │────>│ User       │────>│ Display Results│
│  to Client  │     │ (analysis +   │     │ Interface  │     │ & PDF Viewer   │
└─────────────┘     │  documents)   │     └────────────┘     └────────────────┘
```

**Detailed Flow:**

1. The user enters a query in the web interface
2. JavaScript code sends an AJAX POST request to the `/query` endpoint
3. The FastAPI server (app.py) receives the request and calls the Party class
4. The Party class handles the query in two steps:
   - `retrieve()`: Gets similar documents
   - `analyze()`: Generates analysis
5. Document retrieval process:
   - Check if results exist in the query cache and return if found
   - Check if query embedding exists in cache, otherwise generate and cache it
   - The embedding is compared with stored vectors using cosine similarity
   - Documents are ranked by similarity score
   - The top N documents are returned
   - Actual text is loaded from the PDF only for top results
   - Results are cached for future queries
6. Analysis generation:
   - Token count is estimated for the query and documents
   - Document context is truncated to fit within token limits
   - A prompt is created combining the query and document context
   - The prompt is sent to OpenAI's Chat API with optimized token allocation
   - GPT-4o mini generates a comprehensive analysis
7. The results (analysis and similar documents) are returned to the frontend
8. JavaScript renders the analysis and document cards
9. The most relevant page from the PDF is loaded into the viewer

**Code Flow:**

1. User Interface:
   - Event listener in `index.html` captures user query
   - JavaScript `fetch()` sends request to API endpoint

2. API Handling (`app.py`):
   ```python
   @app.post("/query")
   async def query(query_input: QueryInput):
       similar_docs = party.retrieve(query_input.text)
       analysis = party.analyze(query_input.text, similar_docs)
       return {
           "analysis": analysis,
           "similar_documents": similar_docs
       }
   ```

3. Document Retrieval (`main.py` & `retriever.py`):
   ```python
   def retrieve(self, query):
       return retrieve_similar_documents(query)
   ```

   ```python
   def retrieve_similar_documents(query, top_n=25):
       # Check cache for existing results
       # Get query embedding (from cache if available)
       # Load document references from JSON
       # Calculate similarity scores using cosine.py
       # Get text content from PDF for top results only
       # Cache results for future queries
       # Return top N results
   ```

4. Analysis Generation (`main.py` & `analyzer.py`):
   ```python
   def analyze(self, query, similar_docs):
       return generate_analysis(query, similar_docs)
   ```

   ```python
   def generate_analysis(query, documents):
       # Estimate token counts
       # Truncate context to fit token limits
       # Create prompt with query and document context
       # Generate response using OpenAI
       # Return analysis
   ```

5. Cache Management (`main.py` & `retriever.py`):
   ```python
   def clear_cache(self):
       clear_cache()
       return {"status": "Cache cleared successfully"}
   ```

6. Results Rendering (JavaScript in `index.html`):
   - Processes the returned data
   - Formats and displays the analysis
   - Creates cards for supporting evidence
   - Updates the PDF viewer with the most relevant page

## Data Flow Diagram

The flow of data through the application:

```
┌─────────────────┐      ┌────────────────┐      ┌───────────────┐
│                 │      │                │      │               │
│  Liberal.pdf    │─────>│  Page Text     │─────>│  Embeddings   │
│  (Source)       │      │  (Processing)  │      │  (Vectors)    │
│                 │      │                │      │               │
└─────────────────┘      └────────────────┘      └───────┬───────┘
                                                         │
                                                         │
                                                  ┌──────▼────────┐
                                                  │               │
                                                  │  JSON File    │
                                                  │  Storage      │
                                                  │               │
                                                  └──────┬────────┘
                                                         │
┌─────────────────┐      ┌────────────────┐      ┌──────▼────────┐
│                 │      │                │      │               │
│  User Query     │─────>│  Query Vector  │─────>│  Similarity   │
│  (Text)         │      │  (Embedding)   │      │  Calculation  │
│                 │      │                │      │               │
└─────────────────┘      └────────────────┘      └───────┬───────┘
                                                         │
                                                         │
┌─────────────────┐      ┌────────────────┐      ┌───────▼───────┐
│                 │      │                │      │               │
│  Top Documents  │<─────│  Ranked by     │<─────│  Document     │
│  (Context)      │      │  Relevance     │      │  Scores       │
│                 │      │                │      │               │
└────────┬────────┘      └────────────────┘      └───────────────┘
         │
         │
┌────────▼────────┐      ┌────────────────┐      ┌───────────────┐
│                 │      │                │      │               │
│  User Query +   │─────>│  OpenAI        │─────>│  Analysis     │
│  Context        │      │  GPT Model     │      │  Response     │
│                 │      │                │      │               │
└─────────────────┘      └────────────────┘      └───────┬───────┘
                                                         │
                                                         │
┌─────────────────┐      ┌────────────────┐      ┌───────▼───────┐
│                 │      │                │      │               │
│  UI Elements    │<─────│  HTML/CSS/JS   │<─────│  JSON Data    │
│  (Rendered)     │      │  Rendering     │      │  Response     │
│                 │      │                │      │               │
└─────────────────┘      └────────────────┘      └───────────────┘
```

## Component Dependencies

```
                      ┌───────────────┐
                      │   index.html  │
                      │ (Frontend UI) │
                      └───────┬───────┘
                              │
                              ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ static files  │<────│    app.py     │────>│  /clear-cache │
│ (PDF, CSS)    │     │ (FastAPI App) │     │  /health      │
└───────────────┘     └───────┬───────┘     └───────────────┘
                              │
                              ▼
                      ┌───────────────┐
                      │    main.py    │
                      │ (Party Class) │
                      └───────┬───────┘
                              │
           ┌─────────────────┴───────────────┐
           │                                 │
           ▼                                 ▼
┌───────────────┐                   ┌───────────────┐
│  retriever.py │                   │  analyzer.py  │
│ (Doc Retrieval)│                   │ (AI Analysis) │
└───────┬───────┘                   └───────┬───────┘
        │                                   │
        ▼                                   ▼
┌───────────────┐     ┌───────────────┐    ┌───────────────┐
│ embedding.py  │     │ data_processing│    │   OpenAI API  │
│ (Vectors)     │────>│ (PDF Access)   │    │   (GPT)       │
└───────┬───────┘     └───────────────┘    └───────────────┘
        │                      
        ▼                      
┌───────────────┐              
│   OpenAI API  │              
│  (Embeddings) │              
└───────────────┘              
```

## State Management

SmartVote maintains state in several ways:

1. **Pre-computed Embeddings**:
   - Stored in `document_embeddings.json`
   - Contains page references and their vector representations
   - Does not store full text content (loaded from PDF when needed)
   - Created during the pre-computing phase
   - Reused for all queries

2. **In-Memory Caches**:
   - Query embedding cache: Stores computed embeddings for recent queries
   - Query results cache: Stores results for recent queries
   - Both caches have size limits and basic eviction strategies
   - Can be cleared via API endpoint

3. **Session State (Frontend)**:
   - Current query
   - Retrieved documents
   - Selected PDF page
   - UI state (expanded/collapsed sections)

4. **Server State**:
   - API server maintains no persistent state between requests
   - Each request is processed independently
   - In-memory caches provide performance optimization

## Technologies Used

- **Backend**:
  - FastAPI (API framework)
  - OpenAI API (embeddings and text generation)
  - PyPDF (PDF processing)
  - Python (primary language)
  - NumPy (vector operations)

- **Frontend**:
  - HTML/CSS (UI structure and styling)
  - JavaScript (interactivity and API calls)
  - Fetch API (network requests)
  - PDF.js (built into browsers for PDF rendering)

- **Data Processing**:
  - Vector embeddings (semantic search)
  - Cosine similarity (relevance ranking with NumPy)
  - GPT-4o mini (analysis generation)
  - JSON (data storage)
  - Token optimization (prompt efficiency)
  - Caching (performance optimization)

## Conclusion

The SmartVote application follows a two-phase architecture:
1. A pre-computing phase that processes the PDF and generates embeddings
2. A live query phase that handles user queries and generates responses

This approach allows for efficient semantic search and real-time analysis while keeping the API calls minimal. The separation of document retrieval and analysis generation provides modularity and makes the codebase easier to maintain and extend.

Key optimizations in the architecture include:
1. Memory efficiency through storing only page references and embeddings
2. Lazy loading of text content from PDF files
3. In-memory caching of query embeddings and results
4. Token optimization for prompt generation
5. Efficient error handling and health monitoring

## Performance Profile

Detailed performance testing has been conducted to identify bottlenecks and optimization opportunities. The following chart shows the contribution of each component to the overall query time:

| Component | Time (seconds) | % of Total |
|-----------|---------------:|----------:|
| Query Embedding Generation | 0.68 | 46.2% |
| PDF Text Extraction | 0.63 | 42.8% |
| Loading Embeddings | 0.10 | 7.0% |
| Similarity Calculation | 0.06 | 3.9% |
| Analysis Generation (API) | 0.01 | 0.8% |
| **Total End-to-End** | **1.48** | **100%** |

### Key Performance Insights

1. **Retrieval vs. Analysis**: Document retrieval (99.2%) dominates the total query time, with analysis generation (0.8%) being surprisingly fast.

2. **API Call Distribution**: The embedding generation API call takes significantly longer than the analysis generation API call.

3. **Optimization Impact**: The current optimizations (caching, lazy loading, etc.) already provide significant benefits.

### Performance Optimization Strategy

The performance testing has informed a three-tiered optimization strategy:

1. **Immediate Wins**:
   - Implement PDF text caching
   - Keep embeddings loaded in memory

2. **Medium-term Improvements**:
   - Persistent query embedding cache
   - Pre-extract all PDF text

3. **Long-term Strategy**:
   - Specialized vector databases
   - Client-side embedding generation

For detailed performance analysis and recommendations, refer to the `tests/performance_analysis.md` document. 