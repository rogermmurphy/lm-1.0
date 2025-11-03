#!/usr/bin/env python3
"""
Test Suite for Notifications Service
Tests all 12 endpoints (7 notifications + 5 messages)
"""
import requests
import json

BASE_URL = "http://localhost:8013"
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

# Notification Tests

def test_list_notifications():
    """Test listing notifications"""
    try:
        response = requests.get(f"{BASE_URL}/api/notifications?limit=10")
        passed = response.status_code == 200
        result = response.json() if passed else []
        count = len(result)
        print_test("List Notifications", passed, f"Count: {count}")
        return passed
    except Exception as e:
        print_test("List Notifications", False, str(e))
        return False

def test_get_unread_count():
    """Test getting unread notification count"""
    try:
        response = requests.get(f"{BASE_URL}/api/notifications/unread-count")
        passed = response.status_code == 200
        result = response.json() if passed else {}
        count = result.get("unread_count", 0)
        print_test("Get Unread Count", passed, f"Unread: {count}")
        return passed
    except Exception as e:
        print_test("Get Unread Count", False, str(e))
        return False

def test_get_preferences():
    """Test getting notification preferences"""
    try:
        response = requests.get(f"{BASE_URL}/api/notifications/preferences")
        passed = response.status_code == 200
        result = response.json() if passed else {}
        email = result.get("email_enabled", False)
        push = result.get("push_enabled", False)
        print_test("Get Preferences", passed, f"Email: {email}, Push: {push}")
        return passed
    except Exception as e:
        print_test("Get Preferences", False, str(e))
        return False

def test_update_preferences():
    """Test updating notification preferences"""
    try:
        data = {
            "email_enabled": True,
            "push_enabled": True,
            "assignment_notifications": True,
            "message_notifications": True
        }
        response = requests.put(f"{BASE_URL}/api/notifications/preferences", json=data)
        passed = response.status_code == 200
        print_test("Update Preferences", passed)
        return passed
    except Exception as e:
        print_test("Update Preferences", False, str(e))
        return False

def test_mark_notifications_read():
    """Test marking notifications as read"""
    try:
        # First get some notifications
        response = requests.get(f"{BASE_URL}/api/notifications?limit=5")
        if response.status_code == 200:
            notifications = response.json()
            if notifications:
                notification_ids = [n["id"] for n in notifications[:2]]
                data = {"notification_ids": notification_ids}
                response = requests.post(f"{BASE_URL}/api/notifications/mark-read", json=data)
                passed = response.status_code == 200
                result = response.json() if passed else {}
                count = result.get("count", 0)
                print_test("Mark Notifications Read", passed, f"Marked: {count}")
                return passed
        
        # If no notifications, just test the endpoint
        data = {"notification_ids": []}
        response = requests.post(f"{BASE_URL}/api/notifications/mark-read", json=data)
        passed = response.status_code == 200
        print_test("Mark Notifications Read", passed, "No notifications to mark")
        return passed
    except Exception as e:
        print_test("Mark Notifications Read", False, str(e))
        return False

def test_mark_all_read():
    """Test marking all notifications as read"""
    try:
        response = requests.post(f"{BASE_URL}/api/notifications/mark-all-read")
        passed = response.status_code == 200
        result = response.json() if passed else {}
        count = result.get("count", 0)
        print_test("Mark All Read", passed, f"Marked: {count}")
        return passed
    except Exception as e:
        print_test("Mark All Read", False, str(e))
        return False

def test_delete_notification():
    """Test deleting a notification"""
    try:
        # First get a notification to delete
        response = requests.get(f"{BASE_URL}/api/notifications?limit=1")
        if response.status_code == 200:
            notifications = response.json()
            if notifications:
                notification_id = notifications[0]["id"]
                response = requests.delete(f"{BASE_URL}/api/notifications/{notification_id}")
                passed = response.status_code == 200
                print_test("Delete Notification", passed, f"Deleted ID: {notification_id}")
                return passed
        
        # If no notifications, skip this test
        print_test("Delete Notification", True, "No notifications to delete (skipped)")
        return True
    except Exception as e:
        print_test("Delete Notification", False, str(e))
        return False

# Message Tests

def test_send_message():
    """Test sending a direct message"""
    try:
        data = {
            "recipient_id": 1,  # Send to user 1
            "message": "Hello! This is a test message from the notifications service."
        }
        response = requests.post(f"{BASE_URL}/api/messages/send", json=data)
        passed = response.status_code == 200
        if passed:
            result = response.json()
            message_id = result.get("id")
            print_test("Send Message", passed, f"Message ID: {message_id}")
            return passed, message_id
        else:
            error = response.json().get("detail", "Unknown error")
            print_test("Send Message", False, f"Error: {error}")
            return False, None
    except Exception as e:
        print_test("Send Message", False, str(e))
        return False, None

def test_list_conversations():
    """Test listing conversations"""
    try:
        response = requests.get(f"{BASE_URL}/api/messages/conversations")
        passed = response.status_code == 200
        result = response.json() if passed else []
        count = len(result)
        print_test("List Conversations", passed, f"Count: {count}")
        return passed
    except Exception as e:
        print_test("List Conversations", False, str(e))
        return False

def test_get_conversation():
    """Test getting a conversation with another user"""
    try:
        other_user_id = 1
        response = requests.get(f"{BASE_URL}/api/messages/conversation/{other_user_id}?limit=10")
        passed = response.status_code == 200
        result = response.json() if passed else []
        count = len(result)
        print_test("Get Conversation", passed, f"Messages: {count}")
        return passed
    except Exception as e:
        print_test("Get Conversation", False, str(e))
        return False

def test_mark_messages_read():
    """Test marking messages as read"""
    try:
        # Get conversation to find message IDs
        response = requests.get(f"{BASE_URL}/api/messages/conversation/1?limit=5")
        if response.status_code == 200:
            messages = response.json()
            if messages:
                message_ids = [m["id"] for m in messages[:2] if not m.get("is_read", True)]
                if message_ids:
                    data = {"message_ids": message_ids}
                    response = requests.post(f"{BASE_URL}/api/messages/mark-read", json=data)
                    passed = response.status_code == 200
                    result = response.json() if passed else {}
                    count = result.get("count", 0)
                    print_test("Mark Messages Read", passed, f"Marked: {count}")
                    return passed
        
        # If no unread messages, just test the endpoint
        data = {"message_ids": []}
        response = requests.post(f"{BASE_URL}/api/messages/mark-read", json=data)
        passed = response.status_code == 200
        print_test("Mark Messages Read", passed, "No messages to mark")
        return passed
    except Exception as e:
        print_test("Mark Messages Read", False, str(e))
        return False

def test_delete_message(message_id):
    """Test deleting a message"""
    try:
        if message_id:
            response = requests.delete(f"{BASE_URL}/api/messages/{message_id}")
            passed = response.status_code == 200
            print_test("Delete Message", passed, f"Deleted ID: {message_id}")
            return passed
        else:
            print_test("Delete Message", True, "No message to delete (skipped)")
            return True
    except Exception as e:
        print_test("Delete Message", False, str(e))
        return False

def main():
    """Run all tests"""
    print("=" * 80)
    print("Notifications Service - Test Suite")
    print("=" * 80)
    print()
    
    results = []
    
    # Test 1: Health check
    results.append(test_health())
    print()
    
    # Test 2-8: Notification workflow
    print("Notification Tests:")
    print("-" * 40)
    results.append(test_list_notifications())
    results.append(test_get_unread_count())
    results.append(test_get_preferences())
    results.append(test_update_preferences())
    results.append(test_mark_notifications_read())
    results.append(test_mark_all_read())
    results.append(test_delete_notification())
    print()
    
    # Test 9-13: Message workflow
    print("Message Tests:")
    print("-" * 40)
    passed, message_id = test_send_message()
    results.append(passed)
    
    results.append(test_list_conversations())
    results.append(test_get_conversation())
    results.append(test_mark_messages_read())
    results.append(test_delete_message(message_id))
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
