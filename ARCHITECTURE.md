# SmartVote Architecture and Flow Diagrams

This document provides a detailed explanation of the SmartVote application architecture, including flow diagrams for both the pre-computing phase and the live query phase.

## System Components

SmartVote consists of several key components that work together:

1. **Web Interface** (`index.html`): The frontend that users interact with
2. **API Server** (`app.py`): FastAPI application serving requests
3. **Core Logic** (`main.py`): Contains the Party class with main functionality
4. **Retriever** (`retriever.py`): Handles semantic document retrieval
5. **Analyzer** (`analyzer.py`): Generates policy analysis using OpenAI
6. **Embedding Utility** (`embedding.py`): Creates vector embeddings
7. **Data Processor** (`data_processing.py`): Processes PDF documents and saves as JSON
8. **Vector Math** (`cosine.py`): Provides optimized similarity calculations

## Application Flow

The SmartVote application operates in two distinct phases:

### Phase 1: Pre-computing (PDF Processing and Embedding Generation)

This phase happens before the application serves user queries. It involves processing the PDF document and generating embeddings.

```
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Liberal.pdf│────>│ data_processing│───>│ PyPDF2     │────>│ Extract Text   │
└─────────────┘     │ .py           │     │ Page Reader│     │ from Each Page │
                    └───────┬───────┘     └────────────┘     └────────┬───────┘
                            │                                         │
                            ▼                                         ▼
┌─────────────┐     ┌──────▼──────┐     ┌────────────┐     ┌────────────────┐
│  OpenAI API │<────│ embedding.py│<────│ Process    │<────│ For Each Page  │
│  (Embeddings│     │             │     │ Text       │     │                │
│  Model)     │     └──────┬──────┘     └────────────┘     └────────────────┘
└──────┬──────┘            │
       │                   │
       ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌────────────┐ 
│  Vector     │────>│ Store Data  │────>│ JSON File  │ 
│  Embeddings │     │             │     │            │ 
└─────────────┘     └─────────────┘     └────────────┘ 
```

**Detailed Flow:**

1. The process begins with `data_processing.py`
2. The PDF file (`Liberal.pdf`) is loaded using PyPDF2
3. Text is extracted from each page
4. For each page:
   - The text is processed to remove unwanted characters
   - The text is sent to OpenAI's embedding API through `embedding.py`
   - The returned vector embedding is paired with the text and page number
5. The data is stored in a JSON file (`liberal_with_embeddings.json`)

**Code Flow:**

1. `data_processing.py` (function: `load_and_chunk_pdf()`):
   - Opens the PDF file and creates a PDF reader
   - Loops through each page
   - Extracts text from each page
   - Gets embedding for the text via `embedding.py`
   - Creates a document with page number, text, and embedding
   - Adds the document to a list
   - Saves the list to a JSON file

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
│  retriever  │────>│ Get Query     │────>│ Convert to │────>│ OpenAI API     │
│  .py        │     │ Embedding     │     │ Vector     │     │ (Embeddings)   │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  Load JSON  │────>│ Compare with  │────>│ Rank by    │────>│ Return Top     │
│  Embeddings │     │ Stored Vectors│     │ Similarity │     │ Documents      │
└──────┬──────┘     └───────────────┘     └────────────┘     └────────┬───────┘
       │                                                              │
       ▼                                                              ▼
┌─────────────┐     ┌───────────────┐     ┌────────────┐     ┌────────────────┐
│  analyzer.py│────>│ Generate      │────>│ OpenAI API │────>│ GPT-3.5 Turbo  │
│             │     │ Analysis      │     │ (Chat)     │     │ Model          │
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
   - The query is converted to a vector embedding using OpenAI's API
   - The embedding is compared with stored vectors using cosine similarity
   - Documents are ranked by similarity score
   - The top N documents are returned
6. Analysis generation:
   - The top documents are used as context
   - A prompt is created combining the query and document context
   - The prompt is sent to OpenAI's Chat API
   - GPT-3.5 generates a comprehensive analysis
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
       query_embedding = get_embedding(query)
       # Load documents from JSON
       # Calculate similarity scores using cosine.py
       # Return top N results
   ```

4. Analysis Generation (`main.py` & `analyzer.py`):
   ```python
   def analyze(self, query, similar_docs):
       return generate_analysis(query, similar_docs)
   ```

   ```python
   def generate_analysis(query, documents):
       # Create prompt with query and document context
       # Generate response using OpenAI
       # Return analysis
   ```

5. Results Rendering (JavaScript in `index.html`):
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
┌───────────────┐     ┌───────────────┐
│ static files  │<────│    app.py     │
│ (PDF, CSS)    │     │ (FastAPI App) │
└───────────────┘     └───────┬───────┘
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
┌───────────────┐                   ┌───────────────┐
│ embedding.py  │                   │   OpenAI API  │
│ (Vectors)     │────────────┬─────>│   (GPT)       │
└───────────────┘            │      └───────────────┘
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
   - Stored in `liberal_with_embeddings.json`
   - Contains page texts and their vector representations
   - Created during the pre-computing phase
   - Reused for all queries

2. **Session State (Frontend)**:
   - Current query
   - Retrieved documents
   - Selected PDF page
   - UI state (expanded/collapsed sections)

3. **Server State**:
   - API server maintains no persistent state between requests
   - Each request is processed independently

## Technologies Used

- **Backend**:
  - FastAPI (API framework)
  - OpenAI API (embeddings and text generation)
  - PyPDF2 & PyPDF (PDF processing)
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
  - GPT-3.5 Turbo (analysis generation)
  - JSON (data storage)

## Conclusion

The SmartVote application follows a two-phase architecture:
1. A pre-computing phase that processes the PDF and generates embeddings
2. A live query phase that handles user queries and generates responses

This approach allows for efficient semantic search and real-time analysis while keeping the API calls minimal. The separation of document retrieval and analysis generation provides modularity and makes the codebase easier to maintain and extend. 