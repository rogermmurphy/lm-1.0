"""
Test script for Gamification Service
"""
import requests
import json

BASE_URL = "http://localhost:8011"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_points():
    """Test get points"""
    print("\n=== Testing Get Points ===")
    response = requests.get(f"{BASE_URL}/api/points")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_award_points():
    """Test award points"""
    print("\n=== Testing Award Points ===")
    data = {"points": 10, "reason": "Completed assignment"}
    response = requests.post(f"{BASE_URL}/api/points/award", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_transactions():
    """Test get transactions"""
    print("\n=== Testing Get Transactions ===")
    response = requests.get(f"{BASE_URL}/api/points/transactions")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_achievements():
    """Test achievements"""
    print("\n=== Testing Achievements ===")
    
    # Get achievements
    print("\n1. Get achievements:")
    response = requests.get(f"{BASE_URL}/api/achievements")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Award achievement
    print("\n2. Award achievement:")
    data = {
        "achievement_type": "first_note",
        "achievement_name": "First Note",
        "achievement_description": "Created your first note",
        "points_awarded": 5
    }
    response = requests.post(f"{BASE_URL}/api/achievements", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True

def test_leaderboard():
    """Test leaderboard"""
    print("\n=== Testing Leaderboard ===")
    response = requests.get(f"{BASE_URL}/api/leaderboards/global")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 60)
    print("Gamification Service Test Suite")
    print("=" * 60)
    
    try:
        results = {
            "Health Check": test_health(),
            "Get Points": test_get_points(),
            "Award Points": test_award_points(),
            "Transactions": test_transactions(),
            "Achievements": test_achievements(),
            "Leaderboard": test_leaderboard()
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
        print("\n[ERROR] Could not connect to service. Is it running on port 8011?")
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")

if __name__ == "__main__":
    main()
