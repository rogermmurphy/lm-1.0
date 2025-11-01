#!/usr/bin/env python3
"""
Simple LangChain Agent - Direct implementation without deprecated APIs
Tests: Conversation, RAG tool, Flashcard tool, Presentation tool
"""

from langchain_ollama import OllamaLLM
import sys
import os
import json

# Import existing POC code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../00-functional-poc/backend'))
from rag_chatbot import RAGChatbot
from study_materials import StudyMaterialsGenerator

# Initialize services
rag = RAGChatbot()
materials = StudyMaterialsGenerator()
llm = OllamaLLM(model="llama3.2:3b", base_url="http://localhost:11434", timeout=300)

# Define available tools
TOOLS = {
    "search_content": {
        "description": "Search uploaded educational materials and answer questions",
        "function": lambda query: rag.answer_question(query)['answer']
    },
    "generate_flashcards": {
        "description": "Generate study flashcards on a topic",
        "function": lambda topic: str(materials.generate_flashcards(topic, count=5))
    },
    "create_presentation": {
        "description": "Create a PowerPoint presentation",
        "function": lambda topic: f"Would create presentation on: {topic} (via http://localhost:5000)"
    }
}

def chat(message: str) -> str:
    """Simple agent that decides which tool to use"""
    
    # Build prompt with tool descriptions
    tool_desc = "\n".join([f"- {name}: {info['description']}" for name, info in TOOLS.items()])
    
    prompt = f"""You are an educational AI assistant with access to these tools:

{tool_desc}

User request: {message}

First, decide if you need a tool or can answer directly.
If you need a tool, respond with: USE_TOOL: tool_name | input
Otherwise, just answer the question.

Your response:"""
    
    print(f"\n[AGENT] Processing: {message}")
    response = llm.invoke(prompt)
    
    # Check if agent wants to use a tool
    if "USE_TOOL:" in response:
        parts = response.split("USE_TOOL:")[1].strip().split("|")
        tool_name = parts[0].strip()
        tool_input = parts[1].strip() if len(parts) > 1 else message
        
        if tool_name in TOOLS:
            print(f"[AGENT] Using tool: {tool_name}")
            result = TOOLS[tool_name]["function"](tool_input)
            return f"Tool result: {result}"
    
    return response

if __name__ == "__main__":
    print("="*70)
    print(" Simple LangChain Agent Test")
    print("="*70)
    print()
    
    # Test 1: Simple conversation
    print("\n[TEST 1] Simple conversation")
    result = chat("What is 2+2?")
    print(f"Result: {result[:200]}...")
    
    # Test 2: RAG tool
    print("\n\n[TEST 2] RAG tool (grounded answer)")
    result = chat("What is photosynthesis?")
    print(f"Result: {result[:300]}...")
    
    # Test 3: Flashcard tool  
    print("\n\n[TEST 3] Flashcard generation")
    result = chat("Create flashcards about photosynthesis")
    print(f"Result: {result[:300]}...")
    
    # Test 4: Presentation tool
    print("\n\n[TEST 4] Presentation request")
    result = chat("I want to create a presentation about photosynthesis")
    print(f"Result: {result[:300]}...")
    
    print("\n\n" + "="*70)
    print(" Tests Complete!")
    print("="*70)
