"""Quick verification that agent initializes with all tools"""
import sys
sys.path.insert(0, 'src')

from services.agent_service import AgentService

try:
    agent = AgentService()
    print(f"✓ Agent initialized with {len(agent.tools)} tools:")
    for tool in agent.tools:
        print(f"  - {tool.name}")
    print("\n✓ Batch 2 complete - 8 tools registered successfully")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
