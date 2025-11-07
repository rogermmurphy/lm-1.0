#!/usr/bin/env python3
"""Final verification of all 16 service tools"""
import sys
sys.path.insert(0, 'src')

from src.services.agent_service import AgentService

try:
    agent = AgentService()
    tools = agent.get_available_tools()
    
    print("=" * 80)
    print(f"✓ Agent initialized with {len(tools)} tools")
    print("=" * 80)
    
    # Expected tools by batch
    expected = {
        "Batch 1 - Class Management": ["list_user_classes", "create_class_tool", "add_assignment", "list_assignments", "update_assignment_status"],
        "Batch 2 - AI Study Tools": ["generate_flashcards", "generate_study_notes", "generate_practice_test", "create_flashcards_from_text"],
        "Batch 3 - Content Capture": ["list_my_photos", "list_my_textbooks"],
        "Batch 4 - Social": ["create_study_group", "list_my_study_groups", "list_my_connections"],
        "Batch 5-6 - Analytics & Audio": ["check_my_study_progress", "check_my_points_and_level", "list_my_transcriptions"]
    }
    
    all_good = True
    for batch, batch_tools in expected.items():
        print(f"\n{batch}:")
        for tool in batch_tools:
            if tool in tools:
                print(f"  ✓ {tool}")
            else:
                print(f"  ❌ {tool} - NOT REGISTERED!")
                all_good = False
    
    print("\n" + "=" * 80)
    if all_good and len(tools) == 17:
        print("✅ ALL 17 TOOLS REGISTERED SUCCESSFULLY (16 service + 1 UX enhancement)")
    else:
        print(f"⚠️  Expected 17 tools, found {len(tools)}")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
