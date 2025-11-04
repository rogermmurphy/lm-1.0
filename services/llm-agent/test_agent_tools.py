#!/usr/bin/env python3
"""
Test Agent Tool Calling
Quick test to verify agent can call class management tools
"""
import requests
import json

BASE_URL = "http://localhost:8005/api"

def test_list_classes():
    """Test: User asks to see their classes"""
    print("\n" + "="*70)
    print("TEST 1: List user's classes")
    print("="*70)
    
    response = requests.post(
        f"{BASE_URL}/chat/message",
        json={
            "message": "What classes do I have?",
            "use_rag": False
        },
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\nAI Response:\n{data['response']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_create_class():
    """Test: User asks to create a class"""
    print("\n" + "="*70)
    print("TEST 2: Create a new class")
    print("="*70)
    
    response = requests.post(
        f"{BASE_URL}/chat/message",
        json={
            "message": "Create a class called Physics 101 with teacher Mr. Smith",
            "use_rag": False
        },
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\nAI Response:\n{data['response']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_general_question():
    """Test: General question (no tool needed)"""
    print("\n" + "="*70)
    print("TEST 3: General question (should answer directly)")
    print("="*70)
    
    response = requests.post(
        f"{BASE_URL}/chat/message",
        json={
            "message": "What is 2+2?",
            "use_rag": False
        },
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\nAI Response:\n{data['response']}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    print("\n🚀 Testing Agent Tool Calling POC")
    print("Testing with Bedrock Claude + Class Management Tools\n")
    
    results = []
    
    # Test 1: List classes (tool call)
    results.append(("List Classes", test_list_classes()))
    
    # Test 2: Create class (tool call)
    results.append(("Create Class", test_create_class()))
    
    # Test 3: General question (no tool)
    results.append(("General Question", test_general_question()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, p in results if p)
    total = len(results)
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Agent tool calling is working!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
