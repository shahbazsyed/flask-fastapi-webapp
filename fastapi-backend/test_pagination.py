#!/usr/bin/env python3
"""
Test script to verify pagination functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_pagination():
    """Test pagination on various endpoints"""
    
    print("Testing pagination on FastAPI backend...")
    print("=" * 50)
    
    # Test students endpoint
    print("\n1. Testing /students endpoint:")
    response = requests.get(f"{BASE_URL}/students", params={"skip": 0, "limit": 5})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Response structure: {list(data.keys())}")
        print(f"   ✓ Total students: {data.get('total', 0)}")
        print(f"   ✓ Items returned: {len(data.get('items', []))}")
        print(f"   ✓ Page: {data.get('page', 0)}, Per page: {data.get('per_page', 0)}")
    else:
        print(f"   ✗ Error: {response.status_code}")
    
    # Test courses endpoint
    print("\n2. Testing /courses endpoint:")
    response = requests.get(f"{BASE_URL}/courses", params={"skip": 0, "limit": 3})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Response structure: {list(data.keys())}")
        print(f"   ✓ Total courses: {data.get('total', 0)}")
        print(f"   ✓ Items returned: {len(data.get('items', []))}")
        print(f"   ✓ Page: {data.get('page', 0)}, Per page: {data.get('per_page', 0)}")
    else:
        print(f"   ✗ Error: {response.status_code}")
    
    # Test enrollments endpoint
    print("\n3. Testing /enrollments endpoint:")
    response = requests.get(f"{BASE_URL}/enrollments", params={"skip": 0, "limit": 10})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Response structure: {list(data.keys())}")
        print(f"   ✓ Total enrollments: {data.get('total', 0)}")
        print(f"   ✓ Items returned: {len(data.get('items', []))}")
        print(f"   ✓ Page: {data.get('page', 0)}, Per page: {data.get('per_page', 0)}")
    else:
        print(f"   ✗ Error: {response.status_code}")
    
    # Test pagination with page 2
    print("\n4. Testing pagination (page 2):")
    response = requests.get(f"{BASE_URL}/students", params={"skip": 5, "limit": 5})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Page: {data.get('page', 0)}")
        print(f"   ✓ Items returned: {len(data.get('items', []))}")
    else:
        print(f"   ✗ Error: {response.status_code}")
    
    # Test search with pagination
    print("\n5. Testing search with pagination:")
    response = requests.get(f"{BASE_URL}/courses", params={"skip": 0, "limit": 5, "search": "Math"})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Total matches: {data.get('total', 0)}")
        print(f"   ✓ Items returned: {len(data.get('items', []))}")
    else:
        print(f"   ✗ Error: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("Pagination test complete!")

if __name__ == "__main__":
    test_pagination()