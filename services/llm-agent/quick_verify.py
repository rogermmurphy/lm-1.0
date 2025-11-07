#!/usr/bin/env python3
"""Quick tool verification"""
import sys
sys.path.insert(0, 'src')

from src.services.agent_service import AgentService

try:
    agent = AgentService()
    tools = agent.get_available_tools()
    print(f"✓ Agent initialized with {len(tools)} tools:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool}")
    
    # Check for Batch 3 tools
    batch3_tools = ["list_my_photos", "list_my_textbooks"]
    for tool in batch3_tools:
        if tool in tools:
            print(f"✓ Batch 3 tool '{tool}' registered")
        else:
            print(f"❌ Batch 3 tool '{tool}' NOT registered!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
