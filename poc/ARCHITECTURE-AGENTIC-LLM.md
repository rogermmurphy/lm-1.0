# Agentic LLM Architecture for Your Platform
## How to Let LLM Call APIs (Presenton, RAG, etc.)

**Your Use Case**: User says "Take that lecture and make a presentation about test topics" → LLM calls Presenton API

---

## The Right Approach: Function Calling (Not MCP)

### Why NOT MCP Server?
- **MCP is for tool providers**, not for your application
- Adds unnecessary complexity
- Ollama doesn't natively support MCP
- Standard function calling is simpler and better

### Why Function Calling? ✅
- **Standard pattern** used by OpenAI, Anthropic, Claude
- **Llama 3.2 supports it** natively
- **Simple to implement**
- **Flexible** - add any API as a "function"
- **Already proven** pattern

---

## How It Works

### Architecture
```
User: "Make a presentation from this lecture about photosynthesis"
    ↓
Your Backend
    ↓
LLM with Function Definitions:
  - create_presentation(topic, source, slides)
  - generate_flashcards(topic, count)
  - search_content(query)
  - generate_quiz(topic, count)
    ↓
LLM Returns: Call create_presentation(topic="photosynthesis", source="lecture", slides=10)
    ↓
Your Backend Executes: POST to Presenton API
    ↓
Return Result to User
```

### Example Implementation

```python
# Define available functions/tools
functions = [
    {
        "name": "create_presentation",
        "description": "Create a PowerPoint presentation from content",
        "parameters": {
            "topic": "string - The presentation topic",
            "source_content": "string - The lecture/transcript to use",
            "num_slides": "integer - Number of slides (default: 10)",
            "focus": "string - What to emphasize (e.g., 'test topics', 'key concepts')"
        }
    },
    {
        "name": "generate_flashcards",
        "description": "Generate study flashcards from content",
        "parameters": {
            "topic": "string - The topic",
            "content": "string - Source content",
            "count": "integer - Number of flashcards"
        }
    },
    {
        "name": "search_lectures",
        "description": "Search through uploaded lectures and notes",
        "parameters": {
            "query": "string - What to search for"
        }
    }
]

# Send to LLM with user prompt
prompt = f"""You are an educational AI assistant. You have access to these functions:

{json.dumps(functions, indent=2)}

User request: {user_message}

If you need to call a function, respond with:
FUNCTION_CALL: {{
  "name": "function_name",
  "parameters": {{...}}
}}

Otherwise, respond normally.
"""

# LLM responds with function call
response = ollama.generate(model="llama3.2:3b", prompt=prompt)

# Parse and execute
if "FUNCTION_CALL:" in response:
    function_call = parse_function_call(response)
    if function_call['name'] == 'create_presentation':
        # Call Presenton API
        result = requests.post('http://localhost:5000/api/create', 
                              json=function_call['parameters'])
    # Return result
```

---

## Your Specific Use Case

### User Says: "Make a presentation from this lecture about test topics"

**Step 1**: Your backend receives this + lecture transcript

**Step 2**: Send to LLM with function definitions:
```python
system_prompt = """You have access to:
- create_presentation(topic, content, focus) - Generate PowerPoint
- generate_flashcards(topic, content, count) - Create study cards
- generate_quiz(topic, content, count) - Create quiz
- search_content(query) - Search uploaded materials

User: "Make a presentation from this lecture about test topics"
Lecture: [transcript here]

What should you do?"""
```

**Step 3**: LLM responds:
```json
{
  "function": "create_presentation",
  "parameters": {
    "topic": "Photosynthesis - Test Focus",
    "content": "[lecture transcript]",
    "focus": "facts likely to appear on test",
    "num_slides": 8
  }
}
```

**Step 4**: Your backend calls Presenton API with these parameters

**Step 5**: Return generated presentation to user

---

## Implementation Pattern

### Simple Approach (Good for POC)
Give LLM descriptions of what it can do in the system prompt. Parse its response for action keywords.

```python
system_prompt = """You are an educational AI. You can:

1. Create presentations - When user wants a presentation, extract:
   - Topic
   - Source content
   - Focus area
   Then I'll call the presentation API.

2. Generate flashcards - Extract topic and count

3. Generate quizzes - Extract topic and question count

Respond with structured action in this format:
ACTION: create_presentation
TOPIC: [topic]
CONTENT: [content]
FOCUS: [what to emphasize]
"""
```

### Advanced Approach (For Production)
Use proper function calling with OpenAI-compatible format (Llama 3.2 supports this).

---

## Do You Need MCP?

**No** - MCP is for:
- Exposing YOUR tools TO other AI systems
- Example: Cline using your tools

**For your use case**, you want:
- YOUR LLM using YOUR APIs
- This is just function calling / agentic behavior
- Much simpler than MCP

---

## With Better Hardware

When you get GPU/better PC:
- Same architecture works
- Just faster responses (seconds not minutes)
- Everything else stays the same
- Your code is already set up for this

---

## Recommended Architecture

```
┌─────────────────────────────────────────┐
│  Your Application                        │
│  - User chat interface                   │
│  - Handles user requests                 │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Orchestration Layer (Your Backend)     │
│  - Receives user message                 │
│  - Adds function definitions             │
│  - Calls Ollama                          │
│  - Parses LLM response                   │
│  - Executes API calls                    │
│  - Returns results                       │
└─────────────────────────────────────────┘
        ↓                    ↓
┌──────────────┐    ┌──────────────────┐
│  Ollama LLM  │    │  Your APIs       │
│  (Planning)  │    │  - Presenton     │
└──────────────┘    │  - Flashcards    │
                    │  - RAG Search    │
                    │  - Quiz Gen      │
                    └──────────────────┘
```

---

## Next Steps

1. **For POC**: Use simple keyword parsing
   - If user says "presentation" → call Presenton
   - If user says "flashcards" → call flashcard generator

2. **For Production**: Implement proper function calling
   - Use Llama 3.2's function calling capabilities
   - More robust and flexible

---

## Example Code Structure

```python
class EducationalAgent:
    def __init__(self):
        self.llm = OllamaLLM("llama3.2:3b")
        self.presenton = PresentonAPI("http://localhost:5000")
        self.rag = RAGChatbot()
        self.flashcards = FlashcardGenerator()
    
    async def handle_request(self, user_message, context):
        # Add function definitions to prompt
        prompt = self.build_prompt_with_functions(user_message, context)
        
        # Get LLM decision
        response = await self.llm.generate(prompt)
        
        # Parse for function calls
        if self.is_function_call(response):
            function = self.parse_function_call(response)
            
            # Execute appropriate API
            if function['name'] == 'create_presentation':
                result = await self.presenton.create(**function['params'])
            elif function['name'] == 'generate_flashcards':
                result = await self.flashcards.generate(**function['params'])
            # ... etc
            
            return result
        else:
            return response  # Normal chat response
```

---

## Verdict

**Use Function Calling, NOT MCP**

- ✅ Simpler
- ✅ Standard pattern
- ✅ Llama 3.2 supports it
- ✅ Works with any LLM later
- ✅ Easy to extend

**MCP is overkill for this.**

---

**Status**: Architecture clear, implementation pattern defined
