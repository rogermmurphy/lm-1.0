#!/usr/bin/env python3
"""
Complete Workflow Test - Tests the entire educational AI chatbot system
This demonstrates: Load content → Ask questions → Generate flashcards → Generate quiz
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from content_loader import ContentLoader
from rag_chatbot import RAGChatbot
from study_materials import StudyMaterialsGenerator

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_full_workflow():
    """Run complete end-to-end test"""
    
    print_section("FUNCTIONAL POC - Complete Workflow Test")
    
    # Sample educational content about photosynthesis
    sample_content = """
    PHOTOSYNTHESIS - A COMPLETE GUIDE
    
    What is Photosynthesis?
    Photosynthesis is the process by which green plants, algae, and some bacteria 
    convert light energy (usually from the sun) into chemical energy stored in 
    glucose molecules. This process is fundamental to life on Earth.
    
    The Photosynthesis Equation:
    6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂
    (Carbon dioxide + Water + Light Energy → Glucose + Oxygen)
    
    Two Main Stages:
    
    1. Light-Dependent Reactions (Light Reactions)
       - Occur in the thylakoid membranes of chloroplasts
       - Require light energy
       - Water molecules are split (photolysis)
       - Oxygen is released as a byproduct
       - ATP and NADPH are produced
    
    2. Light-Independent Reactions (Calvin Cycle)
       - Occur in the stroma of chloroplasts
       - Do not require direct light
       - Use ATP and NADPH from light reactions
       - Fix carbon dioxide into glucose
       - This is where sugar is actually made
    
    Key Components:
    - Chlorophyll: Green pigment that absorbs light energy
    - Chloroplasts: Organelles where photosynthesis occurs
    - Stomata: Pores in leaves that allow gas exchange
    - Guard cells: Control the opening and closing of stomata
    
    Importance of Photosynthesis:
    1. Produces oxygen for respiration
    2. Creates glucose for plant energy and growth
    3. Forms the base of most food chains
    4. Removes carbon dioxide from the atmosphere
    5. Stores solar energy in chemical bonds
    
    Factors Affecting Photosynthesis:
    - Light intensity: More light increases the rate (up to a point)
    - Carbon dioxide concentration: More CO₂ increases the rate
    - Temperature: Optimal range is 25-35°C
    - Water availability: Essential for the process
    - Chlorophyll concentration: More chlorophyll means more absorption
    """
    
    # Step 1: Load content into ChromaDB
    print_section("STEP 1: Loading Educational Content")
    try:
        loader = ContentLoader()
        chunks = loader.load_text_content(
            content=sample_content,
            source_name="photosynthesis_guide",
            metadata={"subject": "biology", "topic": "photosynthesis"}
        )
        print(f"[OK] Successfully loaded {chunks} chunks into ChromaDB")
    except Exception as e:
        print(f"[ERROR] Error loading content: {e}")
        return False
    
    # Step 2: Test RAG Chatbot
    print_section("STEP 2: Testing RAG Chatbot")
    try:
        chatbot = RAGChatbot()
        
        questions = [
            "What is photosynthesis?",
            "What are the two main stages of photosynthesis?",
            "Where does the Calvin Cycle occur?",
            "What factors affect the rate of photosynthesis?"
        ]
        
        for question in questions:
            result = chatbot.answer_question(question, collection_name="education")
            print(f"\nQ: {question}")
            print(f"A: {result['answer'][:200]}...")
            if result['sources']:
                print(f"Sources: {len(result['sources'])} documents used")
    except Exception as e:
        print(f"[ERROR] Error in chatbot: {e}")
        return False
    
    # Step 3: Generate Flashcards
    print_section("STEP 3: Generating Flashcards")
    try:
        generator = StudyMaterialsGenerator()
        
        # Search for context
        search_results = chatbot.search_content("photosynthesis", n_results=3)
        context = "\n\n".join(search_results['documents'][0]) if search_results['documents'] else None
        
        flashcards = generator.generate_flashcards(
            topic="photosynthesis",
            context=context,
            count=5
        )
        
        print(f"\n[OK] Generated {len(flashcards)} flashcards:\n")
        for i, card in enumerate(flashcards[:3], 1):  # Show first 3
            print(f"Card {i}:")
            print(f"  Q: {card['question']}")
            print(f"  A: {card['answer']}\n")
        
        if len(flashcards) > 3:
            print(f"  ... and {len(flashcards) - 3} more cards")
    except Exception as e:
        print(f"[ERROR] Error generating flashcards: {e}")
        return False
    
    # Step 4: Generate Quiz
    print_section("STEP 4: Generating Quiz")
    try:
        quiz = generator.generate_quiz(
            topic="photosynthesis",
            context=context,
            count=3,
            difficulty="medium"
        )
        
        print(f"\n[OK] Generated {len(quiz)} quiz questions:\n")
        for i, q in enumerate(quiz, 1):
            print(f"Question {i}: {q['question']}")
            for letter in ['A', 'B', 'C', 'D']:
                if letter in q.get('options', {}):
                    print(f"  {letter}) {q['options'][letter]}")
            print(f"  Answer: {q.get('correct_answer', 'N/A')}\n")
    except Exception as e:
        print(f"[ERROR] Error generating quiz: {e}")
        return False
    
    # Step 5: Success Summary
    print_section("WORKFLOW TEST COMPLETE!")
    print("All components working:")
    print("  [OK] Content loading into ChromaDB")
    print("  [OK] RAG chatbot answering questions")
    print("  [OK] Flashcard generation")
    print("  [OK] Quiz generation")
    print("\n*** The functional POC is working! ***")
    print("\nNext steps:")
    print("  1. Load your own educational content")
    print("  2. Test with real study materials")
    print("  3. Build a simple web interface")
    print("  4. Add more features (PDF upload, etc.)")
    
    return True

if __name__ == "__main__":
    try:
        success = test_full_workflow()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
