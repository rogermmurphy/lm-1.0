#!/usr/bin/env python3
"""
LangChain Agent - Orchestrates educational AI tools
Wraps existing POC code as LangChain tools
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_ollama import OllamaLLM
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import sys
import os
import requests

# Import existing POC code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../00-functional-poc/backend'))
from rag_chatbot import RAGChatbot
from study_materials import StudyMaterialsGenerator

# Initialize services
print("[INIT] Initializing educational AI services...")
rag = RAGChatbot()
materials = StudyMaterialsGenerator()
print("[OK] Services initialized\n")

# Define tool functions
def search_tool(query: str) -> str:
    """Search educational content in vector database"""
    print(f"[TOOL] Using search_content tool...")
    try:
        result = rag.answer_question(query, collection_name="education")
        answer = result['answer']
        sources = len(result.get('sources', []))
        return f"{answer}\n\n(Used {sources} sources from educational content)"
    except Exception as e:
        return f"Error searching content: {e}"

def flashcard_tool(topic: str) -> str:
    """Generate flashcards on a topic"""
    print(f"[TOOL] Using generate_flashcards tool...")
    try:
        # Search for context first
        search_results = rag.search_content(topic, n_results=3)
        context = "\n\n".join(search_results['documents'][0]) if search_results['documents'] else None
        
        # Generate flashcards
        cards = materials.generate_flashcards(topic, context=context, count=5)
        
        # Format response
        result = f"Generated {len(cards)} flashcards on {topic}:\n\n"
        for i, card in enumerate(cards[:3], 1):
            result += f"{i}. Q: {card['question']}\n   A: {card['answer']}\n\n"
        if len(cards) > 3:
            result += f"...and {len(cards) - 3} more flashcards"
        
        return result
    except Exception as e:
        return f"Error generating flashcards: {e}"

def quiz_tool(topic: str) -> str:
    """Generate quiz questions on a topic"""
    print(f"[TOOL] Using generate_quiz tool...")
    try:
        # Search for context
        search_results = rag.search_content(topic, n_results=3)
        context = "\n\n".join(search_results['documents'][0]) if search_results['documents'] else None
        
        # Generate quiz
        questions = materials.generate_quiz(topic, context=context, count=3)
        
        # Format response
        result = f"Generated {len(questions)} quiz questions on {topic}:\n\n"
        for i, q in enumerate(questions, 1):
            result += f"{i}. {q['question']}\n"
            for letter in ['A', 'B', 'C', 'D']:
                if letter in q.get('options', {}):
                    result += f"   {letter}) {q['options'][letter]}\n"
            result += f"   Answer: {q.get('correct_answer', 'N/A')}\n\n"
        
        return result
    except Exception as e:
        return f"Error generating quiz: {e}"

def presentation_tool(topic: str) -> str:
    """Create a presentation on a topic"""
    print(f"[TOOL] Using create_presentation tool...")
    try:
        # Note: This would call Presenton API, but it's very slow
        # For POC, just return a placeholder
        return f"[Presenton would create presentation on: {topic}]\n(Skipped for POC - takes 10-20 minutes on CPU)\n\nTo actually create, visit http://localhost:5000 and enter topic manually."
    except Exception as e:
        return f"Error creating presentation: {e}"

# Create LangChain tools
tools = [
    Tool(
        name="search_educational_content",
        func=search_tool,
        description="Search through uploaded educational materials (textbooks, lectures, notes) and answer questions. Use this when the user asks about content they've uploaded or wants information from their study materials."
    ),
    Tool(
        name="generate_flashcards",
        func=flashcard_tool,
        description="Generate study flashcards on a specific topic. Use this when the user wants to create flashcards to help them study a subject."
    ),
    Tool(
        name="generate_quiz",
        func=quiz_tool,
        description="Generate quiz questions on a topic. Use this when the user wants to test their knowledge with quiz questions."
    ),
    Tool(
        name="create_presentation",
        func=presentation_tool,
        description="Create a PowerPoint presentation on a topic. Use this when the user wants to make a presentation or slides."
    )
]

# Initialize Ollama LLM
print("[INIT] Connecting to Ollama...")
llm = OllamaLLM(
    model="llama3.2:3b",
    base_url="http://localhost:11434",
    temperature=0.7,
    timeout=300
)
print("[OK] Connected to Ollama (llama3.2:3b)\n")

# Create prompt template for ReAct agent
print("[INIT] Creating LangChain agent...")
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# Create ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Wrap in executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)
print("[OK] Agent ready!\n")

def chat(message: str) -> str:
    """Send message to agent and get response"""
    try:
        print(f"{'='*70}")
        print(f"USER: {message}")
        print(f"{'='*70}\n")
        
        result = agent_executor.invoke({"input": message})
        response = result.get("output", "No response")
        
        print(f"\n{'='*70}")
        print(f"AGENT: {response}")
        print(f"{'='*70}\n")
        
        return response
    except Exception as e:
        error_msg = f"Error: {e}"
        print(f"\n[ERROR] {error_msg}")
        return error_msg

if __name__ == "__main__":
    print("="*70)
    print(" LangChain Educational AI Agent")
    print("="*70)
    print()
    
    if len(sys.argv) > 1:
        # Command line mode
        message = " ".join(sys.argv[1:])
        chat(message)
    else:
        # Interactive mode
        print("Interactive mode. Type 'exit' to quit.")
        print()
        while True:
            try:
                message = input("You: ")
                if message.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    break
                chat(message)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
