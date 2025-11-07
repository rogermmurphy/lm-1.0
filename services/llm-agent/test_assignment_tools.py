"""
Test script for assignment management tools
Tests the three new tools: add_assignment, list_assignments, update_assignment_status
"""
import sys
import os
import json
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, 'src')

from tools.class_tools import add_assignment, list_assignments, update_assignment_status, list_user_classes
from src.services.agent_service import AgentService

def print_section(title):
    """Print a section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_individual_tools():
    """Test each tool individually"""
    print_section("TESTING TOOLS INDIVIDUALLY")
    
    # Test 1: List classes (to get class_id)
    print("Test 1: List existing classes")
    try:
        result = list_user_classes.invoke({})
        print(f"✓ list_user_classes result:\n{result}\n")
        
        # Parse class_id from result if available
        # Look for pattern "ID: X)"
        import re
        class_ids = re.findall(r'ID: (\d+)\)', result)
        if class_ids:
            class_id = int(class_ids[0])
            print(f"Found class_id: {class_id}")
        else:
            class_id = 1  # Default
            print(f"No classes found, using default class_id: {class_id}")
    except Exception as e:
        print(f"✗ Error: {e}")
        class_id = 1
    
    # Test 2: Add assignment
    print("\nTest 2: Add new assignment")
    try:
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        result = add_assignment.invoke({
            "class_id": class_id,
            "title": "Test Homework",
            "due_date": due_date,
            "description": "This is a test assignment created by the test script",
            "assignment_type": "homework",
            "priority": "medium"
        })
        print(f"✓ add_assignment result:\n{result}\n")
        
        # Extract assignment_id from result
        assignment_ids = re.findall(r'ID: (\d+)\)', result)
        if assignment_ids:
            assignment_id = int(assignment_ids[0])
            print(f"Created assignment_id: {assignment_id}")
        else:
            assignment_id = None
    except Exception as e:
        print(f"✗ Error: {e}")
        assignment_id = None
    
    # Test 3: List all assignments
    print("\nTest 3: List all assignments")
    try:
        result = list_assignments.invoke({})
        print(f"✓ list_assignments result:\n{result}\n")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 4: List assignments for specific class
    print(f"\nTest 4: List assignments for class_id {class_id}")
    try:
        result = list_assignments.invoke({"class_id": class_id})
        print(f"✓ list_assignments (filtered) result:\n{result}\n")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 5: Update assignment status
    if assignment_id:
        print(f"\nTest 5: Update assignment {assignment_id} to 'completed'")
        try:
            result = update_assignment_status.invoke({
                "assignment_id": assignment_id,
                "new_status": "completed"
            })
            print(f"✓ update_assignment_status result:\n{result}\n")
        except Exception as e:
            print(f"✗ Error: {e}")
    else:
        print("\nTest 5: Skipping (no assignment_id available)")
    
    # Test 6: List completed assignments
    print("\nTest 6: List completed assignments")
    try:
        result = list_assignments.invoke({"status_filter": "completed"})
        print(f"✓ list_assignments (status=completed) result:\n{result}\n")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    return assignment_id

def test_through_agent():
    """Test tools through the agent with natural language"""
    print_section("TESTING THROUGH AGENT WITH NATURAL LANGUAGE")
    
    try:
        agent = AgentService()
        print("✓ AgentService initialized successfully\n")
    except Exception as e:
        print(f"✗ Error initializing agent: {e}")
        return
    
    # Test scenarios
    test_cases = [
        {
            "name": "List my classes",
            "message": "show me my classes",
            "use_rag": False
        },
        {
            "name": "Add assignment",
            "message": "I have homework due next Friday for my first class",
            "use_rag": False
        },
        {
            "name": "List all assignments",
            "message": "what assignments do I have?",
            "use_rag": False
        },
        {
            "name": "List pending assignments",
            "message": "show me my pending assignments",
            "use_rag": False
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"User message: '{test['message']}'")
        try:
            response = agent.chat(test['message'], use_rag=test['use_rag'])
            print(f"Agent response:\n{response}\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")

def test_error_scenarios():
    """Test error handling"""
    print_section("TESTING ERROR SCENARIOS")
    
    # Test 1: Invalid class_id
    print("Test 1: Add assignment with invalid class_id")
    try:
        result = add_assignment.invoke({
            "class_id": 99999,
            "title": "Test",
            "due_date": datetime.now().isoformat()
        })
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"✗ Exception raised: {e}\n")
    
    # Test 2: Invalid assignment_id
    print("Test 2: Update non-existent assignment")
    try:
        result = update_assignment_status.invoke({
            "assignment_id": 99999,
            "new_status": "completed"
        })
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"✗ Exception raised: {e}\n")
    
    # Test 3: Invalid status
    print("Test 3: Update with invalid status")
    try:
        result = update_assignment_status.invoke({
            "assignment_id": 1,
            "new_status": "invalid_status"
        })
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"✗ Exception raised: {e}\n")
    
    # Test 4: Invalid date format
    print("Test 4: Add assignment with invalid date")
    try:
        result = add_assignment.invoke({
            "class_id": 1,
            "title": "Test",
            "due_date": "not a date"
        })
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"✗ Exception raised: {e}\n")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "ASSIGNMENT TOOLS TEST SUITE" + " "*31 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Run tests
        assignment_id = test_individual_tools()
        test_through_agent()
        test_error_scenarios()
        
        # Summary
        print_section("TEST SUMMARY")
        print("✓ Individual tool tests completed")
        print("✓ Agent integration tests completed")
        print("✓ Error scenario tests completed")
        if assignment_id:
            print(f"\nNote: Created test assignment ID {assignment_id}")
            print("You may want to clean this up manually if needed.")
        
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
