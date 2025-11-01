#!/usr/bin/env python3
"""
LangChain Agent with Bedrock Support
Switch between Ollama (local) and Bedrock (cloud) for testing tool calling
"""

from langchain_aws import ChatBedrock
from langchain_ollama import OllamaLLM
import sys
import os

# Import existing POC code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../00-functional-poc/backend'))
from rag_chatbot import RAGChatbot
from study_materials import StudyMaterialsGenerator

# AWS Bedrock credentials (use environment variables in production)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "YOUR_AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "YOUR_AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize services
print("[INIT] Initializing educational AI services...")
rag = RAGChatbot()
materials = StudyMaterialsGenerator()
print("[OK] Services initialized\n")

# Define tool functions
def search_tool(query: str) -> str:
    """Search educational content in vector database"""
    print(f"[TOOL] Executing search_educational_content...")
    try:
        result = rag.answer_question(query, collection_name="education")
        answer = result['answer']
        sources = len(result.get('sources', []))
        return f"{answer}\n\n(Used {sources} sources)"
    except Exception as e:
        return f"Error: {e}"

def flashcard_tool(topic: str) -> str:
    """Generate flashcards"""
    print(f"[TOOL] Executing generate_flashcards...")
    try:
        search_results = rag.search_content(topic, n_results=3)
        context = "\n\n".join(search_results['documents'][0]) if search_results['documents'] else None
        cards = materials.generate_flashcards(topic, context=context, count=5)
        result = f"Created {len(cards)} flashcards:\n"
        for i, card in enumerate(cards[:2], 1):
            result += f"{i}. Q: {card['question']}\n   A: {card['answer']}\n"
        return result
    except Exception as e:
        return f"Error: {e}"

def presentation_tool(topic: str) -> str:
    """Create presentation"""
    print(f"[TOOL] Executing create_presentation...")
    try:
        # Call actual Presenton API
        import requests
        
        print(f"[API] Calling Presenton API to create presentation...")
        response = requests.post(
            'http://localhost:5000/api/v1/ppt/presentation/generate',
            json={
                "content": topic,
                "n_slides": 5,
                "language": "English",
                "template": "general",
                "export_as": "pptx",
                "tone": "educational"
            },
            timeout=600  # 10 minutes for generation
        )
        
        if response.status_code == 200:
            result = response.json()
            presentation_id = result.get('presentation_id', 'unknown')
            edit_path = result.get('edit_path', '')
            
            print(f"[SUCCESS] Presentation created!")
            print(f"  - ID: {presentation_id}")
            print(f"  - Edit URL: http://localhost:5000{edit_path}")
            
            return f"Successfully created presentation on '{topic}'!\n\nPresentation ID: {presentation_id}\nView/Edit: http://localhost:5000{edit_path}\n\n(Note: Generation takes time on CPU - check the link in 5-10 minutes)"
        else:
            return f"Error: Presenton API returned status {response.status_code}\n{response.text}"
            
    except Exception as e:
        return f"Error calling Presenton API: {e}"

# Tool descriptions for prompt
TOOLS_DESC = """Available tools:
- search_educational_content: ONLY use when user asks QUESTIONS about their study materials
- generate_flashcards: ONLY use when user explicitly wants FLASHCARDS for studying
- create_presentation: USE THIS when user wants to CREATE, MAKE, or GENERATE a PRESENTATION, SLIDES, or POWERPOINT

IMPORTANT: If user says "create presentation", "make a presentation", "make slides", or "generate PowerPoint", 
you MUST use the create_presentation tool. Do NOT search for content instead.

To use a tool, respond with: USE_TOOL: tool_name | input"""

def create_llm(use_bedrock=False):
    """Create LLM (Ollama or Bedrock)"""
    if use_bedrock:
        print("[INIT] Connecting to AWS Bedrock...")
        llm = ChatBedrock(
            model_id="anthropic.claude-3-sonnet-20240229-v1:0",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
            model_kwargs={"temperature": 0.7, "max_tokens": 2048}
        )
        print("[OK] Connected to Bedrock (Claude 3 Sonnet)\n")
        return llm
    else:
        print("[INIT] Connecting to Ollama...")
        llm = OllamaLLM(
            model="llama3.2:3b",
            base_url="http://localhost:11434",
            temperature=0.7,
            timeout=300
        )
        print("[OK] Connected to Ollama (llama3.2:3b)\n")
        return llm

def chat(message: str, use_bedrock=False) -> str:
    """Chat with agent"""
    try:
        llm = create_llm(use_bedrock)
        
        # Build prompt
        prompt = f"""{TOOLS_DESC}

User request: {message}

Decide if you need a tool or can answer directly.
If you need a tool, respond with: USE_TOOL: tool_name | input
Otherwise, answer directly.

Response:"""
        
        print(f"[AGENT] Processing request...")
        if use_bedrock:
            response = llm.invoke(prompt).content
        else:
            response = llm.invoke(prompt)
        
        # Check for tool use
        if "USE_TOOL:" in response:
            parts = response.split("USE_TOOL:")[1].strip().split("|")
            tool_name = parts[0].strip()
            tool_input = parts[1].strip() if len(parts) > 1 else message
            
            print(f"[AGENT] Selected tool: {tool_name}")
            
            if "search" in tool_name.lower():
                return search_tool(tool_input)
            elif "flashcard" in tool_name.lower():
                return flashcard_tool(tool_input)
            elif "presentation" in tool_name.lower():
                return presentation_tool(tool_input)
        
        return response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="+", help="Message to send")
    parser.add_argument("--bedrock", action="store_true", help="Use AWS Bedrock instead of Ollama")
    args = parser.parse_args()
    
    message = " ".join(args.message)
    use_bedrock = args.bedrock
    
    model_name = "Bedrock Claude" if use_bedrock else "Ollama llama3.2"
    print(f"\n{'='*70}")
    print(f" Testing with: {model_name}")
    print(f"{'='*70}\n")
    
    response = chat(message, use_bedrock)
    
    print(f"\n{'='*70}")
    print(f"FINAL RESULT:")
    print(f"{'='*70}")
    print(response)
