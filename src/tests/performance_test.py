import time
import json
import os
import sys
import threading
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from functools import partial

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import application modules
from data_processing import process_pdf_and_create_embeddings, get_page_text
from embedding import get_embedding
from retriever import retrieve_similar_documents, clear_cache
from analyzer import generate_analysis
from main import Party

# Set a timeout for each test function using threading.Timer
def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            timeout_flag = {"timed_out": False}
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    exception[0] = e
            
            def on_timeout():
                timeout_flag["timed_out"] = True
                print(f"Function {func.__name__} timed out after {seconds} seconds")
            
            timer = threading.Timer(seconds, on_timeout)
            timer.daemon = True
            timer.start()
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(seconds + 1)  # Wait a bit longer than the timeout
            
            timer.cancel()
            
            if timeout_flag["timed_out"]:
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
            if exception[0] is not None:
                raise exception[0]
            return result[0]
        return wrapper
    return decorator

class PerformanceTest:
    def __init__(self):
        self.results = defaultdict(list)
        # Use absolute paths to data files
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.dirname(self.script_dir)
        self.pdf_path = os.path.join(self.src_dir, "data", "Liberal.pdf")
        self.embeddings_path = os.path.join(self.src_dir, "data", "document_embeddings.json")
        self.test_queries = [
            "housing crisis", 
            "climate change policy",
        ]
        self.output_dir = self.script_dir  # Save output to the current tests directory
        
    def run_comprehensive_tests(self):
        """Run performance tests including Analysis API testing"""
        print("\n======= Running Comprehensive Performance Tests =======")
        
        try:
            # Test text retrieval from PDF
            print("\n=== Testing Text Retrieval Performance ===")
            self.test_text_retrieval(iterations=1)
            
            # Test document retrieval steps
            print("\n=== Testing Document Retrieval Steps ===")
            self.test_retrieval_steps()
            
            # Test analysis generation
            print("\n=== Testing Analysis Generation (OpenAI API) ===")
            self.test_analysis_generation()
            
            # Display results
            self.display_results()
        except Exception as e:
            print(f"Error during tests: {e}")
            # Save partial results
            self.display_results()
    
    @timeout(30)  # 30 second timeout
    def test_retrieval_steps(self):
        """Test individual steps in document retrieval to find bottlenecks"""
        print("Breaking down document retrieval steps...")
        
        # Step 1: Test embedding generation
        clear_cache()
        query = self.test_queries[0]
        print(f"\nTesting embedding generation for query: '{query}'")
        start_time = time.time()
        query_embedding = get_embedding(query)
        end_time = time.time()
        embedding_time = end_time - start_time
        self.results["Query Embedding"].append(embedding_time)
        print(f"  Time: {embedding_time:.4f} seconds")
        
        # Step 2: Test loading embeddings from file
        print("\nTesting loading document embeddings from file")
        start_time = time.time()
        with open(self.embeddings_path, 'r') as f:
            document_embeddings = json.load(f)
        end_time = time.time()
        loading_time = end_time - start_time
        self.results["Loading Embeddings"].append(loading_time)
        print(f"  Time: {loading_time:.4f} seconds")
        print(f"  Number of document embeddings: {len(document_embeddings)}")
        
        # Step 3: Test similarity calculation
        print("\nTesting similarity calculation")
        start_time = time.time()
        similarity_scores = []
        for doc_ref in document_embeddings:
            doc_embedding = doc_ref["embedding"]
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarity_scores.append((doc_ref, similarity))
        end_time = time.time()
        similarity_time = end_time - start_time
        self.results["Similarity Calculation"].append(similarity_time)
        print(f"  Time: {similarity_time:.4f} seconds")
        
        # Step 4: Test sorting and finding top results
        print("\nTesting sorting and finding top results")
        start_time = time.time()
        # Sort by similarity (highest first)
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        # Get top 5 results
        top_results = similarity_scores[:5]
        end_time = time.time()
        sorting_time = end_time - start_time
        self.results["Sorting Results"].append(sorting_time)
        print(f"  Time: {sorting_time:.4f} seconds")
        
        # Step 5: Test text extraction from PDF for top results
        print("\nTesting text extraction for top results")
        start_time = time.time()
        final_results = []
        for doc_ref, score in top_results:
            page_num = doc_ref["page_num"]
            file = doc_ref.get("file", self.pdf_path)
            
            # Use full path for PDF if just filename is stored
            pdf_file_path = file if os.path.exists(file) else self.pdf_path
            
            # Extract text
            try:
                text = get_page_text(pdf_file_path, page_num)
                final_results.append({
                    "page_num": page_num,
                    "similarity": float(score),
                    "text": text
                })
                print(f"    Processed page {page_num}")
            except Exception as e:
                print(f"    Error extracting text from page {page_num}: {e}")
        end_time = time.time()
        extraction_time = end_time - start_time
        self.results["Text Extraction"].append(extraction_time)
        print(f"  Time: {extraction_time:.4f} seconds")
        
        # Calculate total time
        total_time = embedding_time + loading_time + similarity_time + sorting_time + extraction_time
        self.results["Total Retrieval"].append(total_time)
        print(f"\nTotal retrieval time: {total_time:.4f} seconds")
        
        # Return documents for analysis test
        return final_results
        
    @timeout(30)  # 30 second timeout
    def test_text_retrieval(self, iterations=1):
        """Test performance of text retrieval from PDF"""
        print("\nTesting text retrieval from PDF...")
        
        # Get some sample pages to test (reduced number)
        sample_pages = list(range(1, 5))
        
        for i in range(iterations):
            durations = []
            for page in sample_pages:
                try:
                    start_time = time.time()
                    text = get_page_text(self.pdf_path, page)
                    end_time = time.time()
                    durations.append(end_time - start_time)
                    print(f"    Page {page}: Retrieved {len(text)} characters in {end_time - start_time:.4f} seconds")
                except Exception as e:
                    print(f"    Error retrieving text from page {page}: {e}")
                
            if durations:
                avg_duration = sum(durations) / len(durations)
                self.results["Text Retrieval"].append(avg_duration)
                print(f"  Iteration {i+1}: {avg_duration:.4f} seconds per page")
            else:
                print(f"  Iteration {i+1}: No successful text retrieval")
    
    @timeout(120)  # 120 second timeout for the OpenAI API call
    def test_analysis_generation(self):
        """Test performance of analysis generation using OpenAI API"""
        print("\nTesting analysis generation...")
        
        try:
            # Get documents without timing (we'll use the accurate timing from test_retrieval_steps)
            print("Retrieving documents for analysis test...")
            query = self.test_queries[0]
            documents = retrieve_similar_documents(query, top_n=3)
            print(f"  Retrieved {len(documents)} documents")
            
            if not documents:
                print("  No documents found for analysis test, skipping...")
                return
                
            # Test the analysis generation
            print("\nTesting analysis generation with OpenAI API...")
            start_time = time.time()
            analysis = generate_analysis(query, documents)
            api_time = time.time() - start_time
            
            self.results["Analysis Generation (OpenAI API)"].append(api_time)
            print(f"  Analysis generation time: {api_time:.4f} seconds")
            print(f"  Generated analysis with {len(analysis['response'])} characters")
            
            # Compare with retrieval time from the detailed retrieval test
            if "Total Retrieval" in self.results and self.results["Total Retrieval"]:
                retrieval_avg = self.results["Total Retrieval"][0]
                api_ratio = api_time / retrieval_avg
                print(f"\nAPI call is {api_ratio:.2f}x slower than document retrieval")
                print(f"Retrieval: {retrieval_avg:.4f}s vs API: {api_time:.4f}s")
                
                # Calculate end-to-end time
                end_to_end = retrieval_avg + api_time
                self.results["End-to-End Query"].append(end_to_end)
                print(f"Total end-to-end time: {end_to_end:.4f} seconds")
                
                # Calculate percentages
                retrieval_pct = (retrieval_avg / end_to_end) * 100
                api_pct = (api_time / end_to_end) * 100
                print(f"Retrieval: {retrieval_pct:.1f}% of total time")
                print(f"API Call:  {api_pct:.1f}% of total time")
                
        except Exception as e:
            print(f"  Error in analysis generation test: {e}")
            
    def display_results(self):
        """Display performance test results"""
        print("\n======= Performance Test Results =======")
        
        if not self.results:
            print("No results to display")
            return
            
        for component, times in self.results.items():
            if times:
                avg_time = sum(times) / len(times)
                print(f"{component}: {avg_time:.4f} seconds on average")
            
        # Try to create a bar chart if matplotlib is available
        try:
            components = []
            avg_times = []
            
            for component, times in self.results.items():
                if times:
                    components.append(component)
                    avg_times.append(sum(times) / len(times))
                
            if components:
                plt.figure(figsize=(12, 6))
                plt.bar(components, avg_times)
                plt.title('Component Performance Benchmarks')
                plt.xlabel('Component')
                plt.ylabel('Average Time (seconds)')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                chart_path = os.path.join(self.output_dir, 'performance_results.png')
                plt.savefig(chart_path)
                print(f"\nResults chart saved as '{chart_path}'")
        except Exception as e:
            print(f"\nCould not create chart: {e}")
            
        # Save results to JSON
        result_json = os.path.join(self.output_dir, 'performance_results.json')
        with open(result_json, 'w') as f:
            json.dump({k: sum(v)/len(v) for k, v in self.results.items() if v}, f, indent=2)
        print(f"Results saved to '{result_json}'")

if __name__ == "__main__":
    try:
        test = PerformanceTest()
        test.run_comprehensive_tests()
    except KeyboardInterrupt:
        print("\nTest interrupted by user. Saving partial results...")
        if 'test' in locals():
            test.display_results() 