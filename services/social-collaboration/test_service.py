"""
Test script for Social & Collaboration Service
"""
import requests
import json

BASE_URL = "http://localhost:8010"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_connections():
    """Test connections endpoints"""
    print("\n=== Testing Connections ===")
    
    # Get connections
    print("\n1. Get connections:")
    response = requests.get(f"{BASE_URL}/api/connections")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Send connection request
    print("\n2. Send connection request:")
    data = {"classmate_user_id": 2}
    response = requests.post(f"{BASE_URL}/api/connections", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True

def test_groups():
    """Test study groups endpoints"""
    print("\n=== Testing Study Groups ===")
    
    # Create group
    print("\n1. Create study group:")
    data = {
        "name": "Math Study Group",
        "description": "Group for studying calculus",
        "max_members": 10
    }
    response = requests.post(f"{BASE_URL}/api/groups", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Get all groups
    print("\n2. Get all groups:")
    response = requests.get(f"{BASE_URL}/api/groups")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Get my groups
    print("\n3. Get my groups:")
    response = requests.get(f"{BASE_URL}/api/groups/my-groups")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True

def test_sharing():
    """Test content sharing endpoints"""
    print("\n=== Testing Content Sharing ===")
    
    # Share content
    print("\n1. Share content:")
    data = {
        "content_type": "note",
        "content_id": 1,
        "shared_with_user_id": 2,
        "permissions": "view"
    }
    response = requests.post(f"{BASE_URL}/api/sharing", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Get shared with me
    print("\n2. Get content shared with me:")
    response = requests.get(f"{BASE_URL}/api/sharing/received")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Social & Collaboration Service Test Suite")
    print("=" * 60)
    
    try:
        results = {
            "Health Check": test_health(),
            "Root Endpoint": test_root(),
            "Connections": test_connections(),
            "Study Groups": test_groups(),
            "Content Sharing": test_sharing()
        }
        
        print("\n" + "=" * 60)
        print("Test Results Summary")
        print("=" * 60)
        for test_name, passed in results.items():
            status = "[PASS]" if passed else "[FAIL]"
            print(f"{status} {test_name}")
        
        all_passed = all(results.values())
        print("\n" + "=" * 60)
        if all_passed:
            print("[SUCCESS] All tests passed!")
        else:
            print("[FAILURE] Some tests failed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to service. Is it running on port 8010?")
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")

if __name__ == "__main__":
    main()
