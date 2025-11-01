# POC 7: LangChain Agent Integration
## Agentic Chatbot with Tool Orchestration

**Goal**: Integrate LangChain to orchestrate your existing POC tools  
**Time**: 2-3 days  
**Priority**: HIGH

---

## Why LangChain Over MCPHost?

**LangChain is better for your case**:
- ✅ Your POC is already Python (LangChain is Python)
- ✅ Can directly reuse your existing code
- ✅ Built-in RAG support
- ✅ Conversation memory included
- ✅ Production-ready and mature
- ✅ Works with Ollama out of the box
- ✅ Easy to swap LLMs later

---

## Architecture

```
┌──────────────────────────────────────┐
│  User: "Make presentation from        │
│         this lecture about tests"     │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│  Your Backend API                     │
│  - Receives request                   │
│  - Calls LangChain agent              │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│  LangChain Agent (THE ORCHESTRATOR)  │
│  - Decides what tools to use          │
│  - Maintains conversation history     │
│  - Calls Ollama for decisions         │
│  - Executes tools in sequence         │
└──────────────────────────────────────┘
       ↓                ↓               ↓
┌──────────┐  ┌─────────────┐  ┌──────────────┐
│ RAG Tool │  │ Presenton   │  │ Flashcard    │
│          │  │ Tool        │  │ Tool         │
│ (Your    │  │ (Your       │  │ (Your        │
│  POC     │  │  POC        │  │  POC         │
│  code!)  │  │  code!)     │  │  code!)      │
└──────────┘  └─────────────┘  └──────────────┘
```

**You reuse your existing POC code!**

---

## Implementation

### Step 1: Install LangChain

```bash
pip install langchain langchain-community langchain-ollama
```

### Step 2: Wrap Your POC Code as LangChain Tools

```python
# agent.py
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
import sys
import os

# Import your existing POC code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../00-functional-poc/backend'))
from rag_chatbot import RAGChatbot
from study_materials import StudyMaterialsGenerator
import requests

# Initialize your existing services
rag = RAGChatbot()
materials = StudyMaterialsGenerator()

# Wrap as LangChain tools
def search_tool(query: str) -> str:
    """Search educational content in vector database"""
    result = rag.answer_question(query)
    return result['answer']

def flashcard_tool(topic: str) -> str:
    """Generate flashcards on a topic"""
    cards = materials.generate_flashcards(topic, count=5)
    return f"Generated {len(cards)} flashcards on {topic}"

def presentation_tool(input_str: str) -> str:
    """Create a presentation. Input format: 'topic|content|slides'"""
    parts = input_str.split('|')
    topic = parts[0] if len(parts) > 0 else "Topic"
    # Call Presenton API
    try:
        response = requests.post('http://localhost:5000/api/create', json={
            'topic': topic,
            'slides': 5  # Keep it short for POC
        }, timeout=600)
        return f"Created presentation on {topic}"
    except Exception as e:
        return f"Error creating presentation: {e}"

# Create LangChain tools
tools = [
    Tool(
        name="search_content",
        func=search_tool,
        description="Search educational content and get answers from uploaded materials. Use this when user asks questions about their study materials."
    ),
    Tool(
        name="generate_flashcards",
        func=flashcard_tool,
        description="Generate study flashcards on a topic. Use this when user wants to create flashcards for studying."
    ),
    Tool(
        name="create_presentation",
        func=presentation_tool,
        description="Create a PowerPoint presentation. Input should be 'topic|content|slides'. Use this when user wants to make a presentation."
    )
]

# Initialize Ollama LLM
llm = Ollama(
    model="llama3.2:3b",
    base_url="http://localhost:11434",
    timeout=300
)

# Create agent with memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

# Test function
def chat(message: str) -> str:
    """Send message to agent and get response"""
    try:
        response = agent.run(message)
        return response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        print(f"\nUser: {message}")
        print(f"\nAgent: {chat(message)}")
    else:
        print("Usage: python agent.py <your message>")
        print('Example: python agent.py "What is photosynthesis?"')
```

### Step 3: Test the Agent

```bash
cd poc/07-langchain-agent

# Simple question (uses RAG tool)
python agent.py "What is photosynthesis?"

# Generate study materials (uses flashcard tool)
python agent.py "Create 5 flashcards about photosynthesis"

# Complex request (uses multiple tools)
python agent.py "Search for photosynthesis info and make flashcards"
```

---

## What LangChain Gives You

### 1. Automatic Tool Selection
LLM decides which tool to use based on user request.

### 2. Conversation Memory
Remembers chat history automatically.

### 3. Multi-Step Reasoning
Can chain multiple tools: Search → then Create Presentation

### 4. Error Handling
Gracefully handles tool failures.

### 5. Observability
Built-in logging to see what agent is doing.

---

## Integration with Your Backend

```python
# backend_api.py
from fastapi import FastAPI
from agent import agent  # Your LangChain agent

app = FastAPI()

@app.post("/api/chat")
async def chat(message: str, user_id: str):
    # Get user's chat history from database
    history = get_chat_history(user_id)
    
    # Add to agent memory
    for msg in history:
        agent.memory.chat_memory.add_message(msg)
    
    # Run agent
    response = agent.run(message)
    
    # Save to database
    save_chat_message(user_id, message, response)
    
    return {"response": response}
```

---

## Advantages Over Custom Code

### Without LangChain (Custom)
```python
# YOU write all this logic:
if "presentation" in message:
    content = search_content(...)
    create_presentation(content)
elif "flashcard" in message:
    generate_flashcards(...)
elif "quiz" in message:
    generate_quiz(...)
# ... lots of if/else
```

### With LangChain
```python
# LangChain handles it:
response = agent.run(message)
# Agent automatically decides which tools to use!
```

**Much simpler!**

---

## POC 7 Implementation Steps

### Day 1: Setup LangChain
1. Install LangChain packages
2. Create agent.py wrapping your POC code
3. Test with simple queries
4. Verify each tool works

### Day 2: Add Memory & Multi-Tool
1. Add conversation memory
2. Test multi-step workflows
3. Test "search then create presentation"
4. Optimize prompts

### Day 3: Backend Integration
1. Create FastAPI endpoint using agent
2. Add database for chat history
3. Test end-to-end flow
4. Document patterns

---

## Success Criteria

- [ ] LangChain agent running with Ollama
- [ ] Can call your RAG code as tool
- [ ] Can generate flashcards via agent
- [ ] Can create presentations via agent
- [ ] Multi-tool orchestration works
- [ ] Conversation memory works
- [ ] Integrated with backend API

---

## Comparison: All Options

| Framework | Best For | Complexity | Your Fit |
|-----------|----------|------------|----------|
| MCPHost | Simple MCP | Low | ⭐⭐ Good |
| **LangChain** | **Production apps** | **Medium** | **⭐⭐⭐ Best** |
| AutoGen | Multi-agent | High | ⭐ Overkill |
| CrewAI | Multi-agent | High | ⭐ Overkill |

**Recommendation**: LangChain ✅

---

## Next Steps

Want me to:
1. Create the LangChain agent POC code?
2. Test it with your existing POC?
3. Show you how to integrate with backend?

Ready to build POC 7 with LangChain?
</response>
</plan_mode_respond>
