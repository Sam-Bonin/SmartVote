import time
import os
import sys
import random

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retriever import retrieve_similar_documents
from analyzer import generate_analysis
from config import TOP_N_DOCUMENTS

def simulate_network_delay(min_delay=0.5, max_delay=2.0):
    """Simulate variable network delay"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    return delay

def test_real_world_conditions():
    """Test API performance with simulated real-world conditions"""
    print("\n=== Testing API Performance with Simulated Real-World Conditions ===")
    
    # Sample query
    query = "healthcare policy"
    
    # Cold start - first retrieval usually takes longer
    print("\nCold start retrieval:")
    start_time = time.time()
    documents = retrieve_similar_documents(query, top_n=TOP_N_DOCUMENTS)
    retrieval_time = time.time() - start_time
    print(f"  Cold start retrieval time: {retrieval_time:.2f} seconds")
    print(f"  Retrieved {len(documents)} documents")
    
    # Add simulated network delay before API call
    network_delay = simulate_network_delay()
    print(f"\nSimulated network delay: {network_delay:.2f} seconds")
    
    # Test analysis generation with simulated network conditions
    print("\nTesting analysis generation with network delays:")
    start_time = time.time()
    
    # Simulate request delay
    request_delay = simulate_network_delay(0.2, 1.0)
    print(f"  Request transmission delay: {request_delay:.2f} seconds")
    
    # Actual API call
    api_start = time.time()
    analysis = generate_analysis(query, documents)
    api_time = time.time() - api_start
    print(f"  Pure API processing time: {api_time:.2f} seconds")
    
    # Simulate response delay
    response_delay = simulate_network_delay(0.2, 1.0)
    print(f"  Response transmission delay: {response_delay:.2f} seconds")
    
    # Calculate total time
    total_time = time.time() - start_time
    print(f"\nTotal end-to-end time with network simulation: {total_time:.2f} seconds")
    
    # Add frontend rendering estimation
    frontend_delay = random.uniform(0.5, 1.5)
    print(f"Estimated frontend rendering time: {frontend_delay:.2f} seconds")
    
    print(f"Estimated total user experience time: {total_time + frontend_delay:.2f} seconds")
    
    # Show the response length
    print(f"\nGenerated analysis with {len(analysis['response'])} characters")

if __name__ == "__main__":
    test_real_world_conditions() 