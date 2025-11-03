#!/usr/bin/env python3
"""
Test Suite for Study Analytics Service
Tests all 9 endpoints (4 sessions + 5 goals)
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8012"
USER_ID = 7  # Test user

def print_test(name, passed, details=""):
    """Print test result"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"      {details}")

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        passed = response.status_code == 200
        print_test("Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False

def test_start_session():
    """Test starting a study session"""
    try:
        data = {
            "class_id": None,
            "session_type": "solo",
            "focus_mode": True,
            "location": "library"
        }
        response = requests.post(f"{BASE_URL}/api/analytics/sessions/start", json=data)
        passed = response.status_code == 200
        if passed:
            result = response.json()
            session_id = result.get("session_id")
            print_test("Start Session", passed, f"Session ID: {session_id}")
            return passed, session_id
        else:
            error = response.json().get("detail", "Unknown error")
            print_test("Start Session", False, f"Error: {error}")
            return False, None
    except Exception as e:
        print_test("Start Session", False, str(e))
        return False, None

def test_log_activity(session_id):
    """Test logging an activity"""
    try:
        data = {
            "activity_type": "testing",
            "content_type": "test",
            "content_id": 1,
            "items_completed": 20,
            "items_correct": 18,
            "duration_minutes": 30
        }
        response = requests.post(
            f"{BASE_URL}/api/analytics/sessions/{session_id}/activities",
            json=data
        )
        passed = response.status_code == 200
        result = response.json() if passed else {}
        accuracy = result.get("accuracy_percentage")
        points = result.get("points_earned")
        print_test("Log Activity", passed, f"Accuracy: {accuracy}%, Points: {points}")
        return passed
    except Exception as e:
        print_test("Log Activity", False, str(e))
        return False

def test_end_session(session_id):
    """Test ending a study session"""
    try:
        data = {
            "mood_rating": 5,
            "productivity_rating": 4,
            "notes": "Great study session!"
        }
        response = requests.put(
            f"{BASE_URL}/api/analytics/sessions/{session_id}/end",
            json=data
        )
        passed = response.status_code == 200
        result = response.json() if passed else {}
        duration = result.get("duration_minutes")
        points = result.get("points_earned")
        print_test("End Session", passed, f"Duration: {duration}min, Points: {points}")
        return passed
    except Exception as e:
        print_test("End Session", False, str(e))
        return False

def test_list_sessions():
    """Test listing sessions"""
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/sessions?limit=10")
        passed = response.status_code == 200
        result = response.json() if passed else {}
        count = result.get("total_count", 0)
        total_min = result.get("total_minutes", 0)
        print_test("List Sessions", passed, f"Count: {count}, Total: {total_min}min")
        return passed
    except Exception as e:
        print_test("List Sessions", False, str(e))
        return False

def test_create_goal():
    """Test creating a study goal"""
    try:
        today = date.today()
        target = today + timedelta(days=30)
        
        data = {
            "class_id": None,
            "goal_type": "study_time",
            "goal_name": "Study 20 hours this month",
            "goal_description": "Focus on calculus",
            "target_value": 1200,
            "unit": "minutes",
            "start_date": today.isoformat(),
            "target_date": target.isoformat(),
            "priority": "high",
            "is_recurring": False,
            "reminder_enabled": True
        }
        response = requests.post(f"{BASE_URL}/api/analytics/goals", json=data)
        passed = response.status_code == 200
        if passed:
            result = response.json()
            goal_id = result.get("goal_id")
            print_test("Create Goal", passed, f"Goal ID: {goal_id}")
            return passed, goal_id
        else:
            error = response.json().get("detail", "Unknown error")
            print_test("Create Goal", False, f"Error: {error}")
            return False, None
    except Exception as e:
        print_test("Create Goal", False, str(e))
        return False, None

def test_list_goals():
    """Test listing goals"""
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/goals?status=active")
        passed = response.status_code == 200
        result = response.json() if passed else {}
        count = result.get("total_count", 0)
        active = result.get("active_count", 0)
        print_test("List Goals", passed, f"Total: {count}, Active: {active}")
        return passed
    except Exception as e:
        print_test("List Goals", False, str(e))
        return False

def test_record_progress(goal_id):
    """Test recording goal progress"""
    try:
        data = {
            "progress_value": 300,
            "notes": "Made good progress today"
        }
        response = requests.post(
            f"{BASE_URL}/api/analytics/goals/{goal_id}/progress",
            json=data
        )
        passed = response.status_code == 200
        result = response.json() if passed else {}
        percentage = result.get("percentage_complete", 0)
        print_test("Record Progress", passed, f"Progress: {percentage}%")
        return passed
    except Exception as e:
        print_test("Record Progress", False, str(e))
        return False

def test_update_goal(goal_id):
    """Test updating a goal"""
    try:
        data = {
            "priority": "medium",
            "target_value": 1500
        }
        response = requests.put(
            f"{BASE_URL}/api/analytics/goals/{goal_id}",
            json=data
        )
        passed = response.status_code == 200
        print_test("Update Goal", passed)
        return passed
    except Exception as e:
        print_test("Update Goal", False, str(e))
        return False

def test_delete_goal(goal_id):
    """Test deleting a goal"""
    try:
        response = requests.delete(f"{BASE_URL}/api/analytics/goals/{goal_id}")
        passed = response.status_code == 200
        print_test("Delete Goal", passed)
        return passed
    except Exception as e:
        print_test("Delete Goal", False, str(e))
        return False

def main():
    """Run all tests"""
    print("=" * 80)
    print("Study Analytics Service - Test Suite")
    print("=" * 80)
    print()
    
    results = []
    
    # Test 1: Health check
    results.append(test_health())
    print()
    
    # Test 2-5: Session workflow
    print("Session Workflow Tests:")
    print("-" * 40)
    passed, session_id = test_start_session()
    results.append(passed)
    
    if session_id:
        results.append(test_log_activity(session_id))
        results.append(test_end_session(session_id))
    else:
        results.extend([False, False])
    
    results.append(test_list_sessions())
    print()
    
    # Test 6-10: Goal workflow
    print("Goal Workflow Tests:")
    print("-" * 40)
    passed, goal_id = test_create_goal()
    results.append(passed)
    
    results.append(test_list_goals())
    
    if goal_id:
        results.append(test_record_progress(goal_id))
        results.append(test_update_goal(goal_id))
        results.append(test_delete_goal(goal_id))
    else:
        results.extend([False, False, False])
    
    print()
    
    # Summary
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    passed_count = sum(results)
    total_count = len(results)
    pass_rate = (passed_count / total_count * 100) if total_count > 0 else 0
    
    print(f"Passed: {passed_count}/{total_count} ({pass_rate:.1f}%)")
    print()
    
    if passed_count == total_count:
        print("[SUCCESS] All tests passed!")
        return 0
    else:
        print("[FAILURE] Some tests failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    exit(main())
