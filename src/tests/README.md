# SmartVote Performance Testing

This directory contains performance testing tools and results for the SmartVote application.

## Files

- **performance_test.py**: Test script for measuring component performance in controlled conditions
- **network_test.py**: Test script for simulating real-world conditions with network delays
- **performance_analysis.md**: Detailed analysis of performance bottlenecks
- **performance_results.json**: Raw performance data in JSON format
- **performance_results.png**: Chart visualization of performance metrics

## Running the Tests

### Controlled Environment Testing

To run the standard performance tests:

```bash
cd src/tests
python performance_test.py
```

This will:
1. Test performance of text retrieval from PDF
2. Break down document retrieval into individual steps (embedding generation, loading, similarity, etc.)
3. Test analysis generation using the OpenAI API
4. Generate updated performance metrics and save to JSON and PNG

### Real-World Conditions Testing

To simulate real-world conditions including network delays:

```bash
cd src/tests
python network_test.py
```

This will:
1. Measure cold start retrieval time
2. Simulate network delays for request/response transmission
3. Track pure API processing time
4. Estimate frontend rendering time
5. Calculate total user experience time

## Test Methodology

The tests use timeouts and multiple iterations to ensure accurate measurements. Each component is isolated and timed separately:

1. **Text Retrieval**: Measures time to extract text from individual PDF pages
2. **Retrieval Steps**:
   - Query embedding generation (API call)
   - Loading embeddings from JSON
   - Similarity calculation between query and documents
   - Sorting results by relevance
   - Text extraction from PDF for top results
3. **Analysis Generation**: Measures OpenAI API call time for generating analysis
4. **Network Simulation** (network_test.py only):
   - Adds realistic network delays
   - Measures cold start performance
   - Simulates frontend rendering time

## Performance Results

### Controlled Environment Results

The latest test results in a controlled environment show:

| Component | Average Time (seconds) |
|-----------|------------------------|
| Text Retrieval (single page) | 0.11 |
| Query Embedding Generation | 0.68 |
| Loading Embeddings from JSON | 0.10 |
| Similarity Calculation | 0.06 |
| Sorting Results | < 0.01 |
| Text Extraction from PDF (5 pages) | 0.63 |
| **Total Retrieval Process** | **1.47** |
| Analysis Generation (OpenAI API) | 5.29 |
| **End-to-End Query** | **6.76** |

### Real-World Performance Results

When tested with network delays and cold start conditions:

| Component | Time (seconds) |
|-----------|----------------|
| Cold Start Retrieval | 25-30 |
| Network Delays (round trip) | 2-3 |
| API Processing | 5-7 |
| Frontend Rendering | 1-1.5 |
| **Total User Experience** | **33-41.5** |

For a detailed analysis of these results and optimization recommendations, see `performance_analysis.md`. 