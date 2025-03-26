# SmartVote Performance Testing

This directory contains performance testing tools and results for the SmartVote application.

## Files

- **performance_test.py**: Test script for measuring component performance
- **performance_analysis.md**: Detailed analysis of performance bottlenecks
- **performance_results.json**: Raw performance data in JSON format
- **performance_results.png**: Chart visualization of performance metrics

## Running the Tests

To run the performance tests:

```bash
cd src/tests
python performance_test.py
```

This will:
1. Test performance of text retrieval from PDF
2. Break down document retrieval into individual steps (embedding generation, loading, similarity, etc.)
3. Test analysis generation using the OpenAI API
4. Generate updated performance metrics and save to JSON and PNG

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

## Performance Results

The latest test results show:

| Component | Average Time (seconds) |
|-----------|------------------------|
| Text Retrieval (single page) | 0.11 |
| Query Embedding Generation | 0.68 |
| Loading Embeddings from JSON | 0.10 |
| Similarity Calculation | 0.06 |
| Sorting Results | < 0.01 |
| Text Extraction from PDF (5 pages) | 0.63 |
| Analysis Generation (OpenAI API) | 0.01 |
| **End-to-End Query** | **1.48** |

For a detailed analysis of these results and optimization recommendations, see `performance_analysis.md`. 