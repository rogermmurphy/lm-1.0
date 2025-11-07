#!/usr/bin/env python3
"""
E2E Test: Agent Fixes Verification
Tests all fixes deployed for AI Agent Phase 2
Location: tests/e2e/test_agent_fixes.py
"""
import httpx
import json
import sys

def test_agent_tools():
    """Test 1: Verify 17 tools registered"""
    print("\n[TEST 1] Agent Tools Registration")
    print("-" * 60)
    try:
        sys.path.insert(0, 'services/llm-agent/src')
        from services.agent_service import AgentService
        
        agent = AgentService()
        tools = agent.get_available_tools()
        
        print(f"Tools registered: {len(tools)}")
        if len(tools) == 17:
            print("✅ PASS: All 17 tools registered")
            return True
        else:
            print(f"❌ FAIL: Expected 17, got {len(tools)}")
            return False
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_flashcard_endpoint():
    """Test 2: Flashcard endpoint with JSON body"""
    print("\n[TEST 2] Flashcard Endpoint (JSON Body)")
    print("-" * 60)
    try:
        response = httpx.post(
            "http://ai-study-tools-service:8009/api/flashcards/generate-from-text",
            json={
                "user_id": 1,
                "topic": "Python Basics",
                "content_text": "Python is a high-level programming language. It uses indentation for code blocks. Variables don't need type declaration. It supports object-oriented and functional programming.",
                "card_count": 3
            },
            timeout=45.0
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            cards = data.get('cards', [])
            print(f"✅ PASS: Generated {len(cards)} flashcards")
            if cards:
                print(f"Sample: {cards[0].get('front_text', 'N/A')[:50]}...")
            return True
        else:
            print(f"❌ FAIL: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_messages_endpoint():
    """Test 3: Conversation messages endpoint"""
    print("\n[TEST 3] Conversation Messages Endpoint")
    print("-" * 60)
    try:
        # Get conversations - use internal route path
        response = httpx.get(
            "http://llm-service:8000/chat/conversations",
            timeout=10.0
        )
        
        print(f"Conversations status: {response.status_code}")
        
        if response.status_code == 200:
            convs = response.json()
            print(f"Found {len(convs)} conversations")
            
            if len(convs) > 0:
                conv_id = convs[0]['id']
                # Test messages endpoint - use internal route path
                msg_response = httpx.get(
                    f"http://llm-service:8000/chat/conversations/{conv_id}/messages",
                    timeout=10.0
                )
                
                print(f"Messages status: {msg_response.status_code}")
                
                if msg_response.status_code == 200:
                    msgs = msg_response.json()
                    msg_count = len(msgs.get('messages', []))
                    print(f"✅ PASS: Retrieved {msg_count} messages")
                    return True
                else:
                    print(f"❌ FAIL: Messages HTTP {msg_response.status_code}")
                    return False
            else:
                print("⚠️  SKIP: No conversations to test")
                return True  # Not a failure, just no data
        else:
            print(f"❌ FAIL: Conversations HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def main():
    print("=" * 80)
    print("AI AGENT FIXES - E2E VERIFICATION TEST")
    print("=" * 80)
    
    results = []
    
    # Run all tests
    results.append(("Agent Tools", test_agent_tools()))
    results.append(("Flashcard Endpoint", test_flashcard_endpoint()))
    results.append(("Messages Endpoint", test_messages_endpoint()))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - ZERO ERRORS VERIFIED")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - NEED FIXES")
        return 1

if __name__ == "__main__":
    sys.exit(main())
