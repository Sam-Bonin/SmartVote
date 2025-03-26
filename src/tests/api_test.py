#!/usr/bin/env python3
import requests
import json
import sys
import os

# Add the parent directory to the Python path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

API_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        print("✅ Health endpoint returned 200 OK")
        data = response.json()
        print(f"   Response: {data}")
        return True
    else:
        print(f"❌ Health endpoint returned {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_query_endpoint():
    """Test the query endpoint"""
    print("\nTesting query endpoint...")
    query = "healthcare"
    response = requests.post(
        f"{API_URL}/query", 
        json={"text": query}
    )
    
    if response.status_code == 200:
        print(f"✅ Query endpoint returned 200 OK for query: '{query}'")
        data = response.json()
        
        # Check for expected fields
        if "analysis" in data and "similar_documents" in data:
            print("✅ Response contains analysis and similar_documents")
            
            # Check document structure
            if len(data["similar_documents"]) > 0:
                first_doc = data["similar_documents"][0]
                print("\nChecking first document structure:")
                
                # Check required fields for frontend
                required_fields = ["page", "score", "text"]
                missing_fields = [field for field in required_fields if field not in first_doc]
                
                if not missing_fields:
                    print("✅ Document has all required fields for frontend")
                else:
                    print(f"❌ Document missing fields: {missing_fields}")
                
                # Print document fields
                for field, value in first_doc.items():
                    if field == "text":
                        # Truncate long text
                        print(f"   {field}: {value[:50]}... ({len(value)} chars)")
                    else:
                        print(f"   {field}: {value}")
                
                return True
            else:
                print("❌ No documents returned in response")
                return False
        else:
            print(f"❌ Response missing expected fields")
            print(f"   Available fields: {list(data.keys())}")
            return False
    else:
        print(f"❌ Query endpoint returned {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_pdf_access():
    """Test PDF file access"""
    print("\nTesting PDF access...")
    response = requests.head(f"{API_URL}/data/Liberal.pdf")
    
    if response.status_code == 200:
        print("✅ PDF file is accessible")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content-Length: {response.headers.get('Content-Length')} bytes")
        return True
    else:
        print(f"❌ PDF file returned {response.status_code}")
        print(f"   Response headers: {response.headers}")
        return False

if __name__ == "__main__":
    print("====== API Testing ======")
    
    all_tests_passed = True
    
    # Test health endpoint
    if not test_health_endpoint():
        all_tests_passed = False
    
    # Test query endpoint
    if not test_query_endpoint():
        all_tests_passed = False
    
    # Test PDF access
    if not test_pdf_access():
        all_tests_passed = False
    
    print("\n====== Test Summary ======")
    if all_tests_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.") 