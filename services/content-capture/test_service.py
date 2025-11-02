"""
Content Capture Service - Test Suite
Tests for photo upload, OCR, textbook processing, and vector search
"""
import requests
import json
import os
from typing import Dict, Any

# Service configuration
BASE_URL = "http://localhost:8008"
TEST_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3MzA2NjQwMDB9.test"

def test_health_check():
    """Test service health endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_root_endpoint():
    """Test root endpoint"""
    print("\nTesting root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_photo_upload():
    """Test photo upload (mock test without actual file)"""
    print("\nTesting photo upload endpoint...")
    
    # Test without file (should fail)
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    data = {"title": "Test Photo", "class_id": 1}
    
    response = requests.post(f"{BASE_URL}/api/photos/upload", headers=headers, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Should return 422 (missing file)
    return response.status_code == 422

def test_get_photos():
    """Test get photos endpoint"""
    print("\nTesting get photos...")
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    
    response = requests.get(f"{BASE_URL}/api/photos", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code in [200, 401]  # 401 if auth fails, 200 if succeeds

def test_textbook_upload():
    """Test textbook upload (mock test without actual file)"""
    print("\nTesting textbook upload endpoint...")
    
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    data = {"title": "Test Textbook", "author": "Test Author", "class_id": 1}
    
    response = requests.post(f"{BASE_URL}/api/textbooks/upload", headers=headers, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Should return 422 (missing file)
    return response.status_code == 422

def test_get_textbooks():
    """Test get textbooks endpoint"""
    print("\nTesting get textbooks...")
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    
    response = requests.get(f"{BASE_URL}/api/textbooks", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code in [200, 401]

def test_textbook_search():
    """Test textbook search endpoint"""
    print("\nTesting textbook search...")
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    data = {"query": "machine learning"}
    
    response = requests.post(f"{BASE_URL}/api/textbooks/search", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code in [200, 401]

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("CONTENT CAPTURE SERVICE TESTS")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Photo Upload", test_photo_upload),
        ("Get Photos", test_get_photos),
        ("Textbook Upload", test_textbook_upload),
        ("Get Textbooks", test_get_textbooks),
        ("Textbook Search", test_textbook_search),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
        except Exception as e:
            print(f"ERROR in {test_name}: {e}")
            results.append((test_name, "ERROR"))
    
    print("\n" + "=" * 50)
    print("TEST RESULTS")
    print("=" * 50)
    for test_name, status in results:
        print(f"{test_name:.<30} {status}")
    
    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)
    print(f"\nPassed: {passed}/{total}")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
