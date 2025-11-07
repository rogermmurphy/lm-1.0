#!/usr/bin/env python3
"""
Comprehensive test of ALL fixes deployed
Tests every single fix to prove zero errors
"""
import httpx
import json

print("=" * 80)
print("COMPREHENSIVE FIX VERIFICATION TEST")
print("=" * 80)

# Test 1: Agent tools still registered
print("\n[TEST 1] Verifying agent tools...")
try:
    import sys
    sys.path.insert(0, 'src')
    from src.services.agent_service import AgentService
    
    agent = AgentService()
    tools = agent.get_available_tools()
    
    if len(tools) == 17:
        print(f"✅ All 17 tools registered")
    else:
        print(f"❌ Expected 17 tools, got {len(tools)}")
except Exception as e:
    print(f"❌ Agent initialization failed: {e}")

# Test 2: Flashcard endpoint accepts JSON
print("\n[TEST 2] Testing flashcard endpoint with JSON body...")
try:
    response = httpx.post(
        "http://ai-study-tools-service:8009/api/flashcards/generate-from-text",
        json={
            "user_id": 1,
            "topic": "Test Topic",
            "content_text": "This is test content for generating flashcards. It needs to be at least 50 characters long to pass validation.",
            "card_count": 5
        },
        timeout=30.0
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Flashcard endpoint works! Generated {data.get('count', 0)} cards")
        if data.get('cards'):
            print(f"   Sample card: {data['cards'][0].get('front_text', 'N/A')}")
    else:
        print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
        
except httpx.TimeoutException:
    print("⏰ Timeout - Bedrock may be slow or having issues")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Conversation messages endpoint
print("\n[TEST 3] Testing conversation messages endpoint...")
try:
    # First check if there are any conversations
    response = httpx.get(
        "http://localhost:8005/api/chat/conversations",
        timeout=10.0
    )
    
    if response.status_code == 200:
        convs = response.json()
        print(f"✅ Found {len(convs)} conversations")
        
        if len(convs) > 0:
            conv_id = convs[0]['id']
            # Test messages endpoint
            msg_response = httpx.get(
                f"http://localhost:8005/api/chat/conversations/{conv_id}/messages",
                timeout=10.0
            )
            
            if msg_response.status_code == 200:
                msgs = msg_response.json()
                print(f"✅ Messages endpoint works! Got {len(msgs.get('messages', []))} messages")
            else:
                print(f"❌ Messages endpoint failed: HTTP {msg_response.status_code}")
        else:
            print("ℹ️  No conversations to test messages endpoint")
    else:
        print(f"❌ Conversations endpoint failed: HTTP {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Verify service is using correct Bedrock model
print("\n[TEST 4] Checking Bedrock model configuration...")
try:
    from src.services.ai_service import AIService
    ai = AIService()
    print(f"✅ ai-study-tools using model: {ai.model_id}")
    
    if "claude-sonnet-4" in ai.model_id:
        print("✅ Correct model ID format")
    else:
        print(f"⚠️  Model may need updating: {ai.model_id}")
except Exception as e:
    print(f"❌ Can't check AI service: {e}")

print("\n" + "=" * 80)
print("TEST COMPLETE - Review results above")
print("=" * 80)
