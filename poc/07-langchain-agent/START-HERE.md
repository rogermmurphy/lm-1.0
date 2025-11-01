# LangChain Agent POC - Quick Start

**Goal**: Validate agent can converse, use RAG, and orchestrate tools

---

## What This Tests

### Test 1: Simple Conversation ✅
**User**: "What is 2+2?"  
**Expected**: Agent answers basic questions

### Test 2: Grounded Knowledge ✅
**User**: "What is photosynthesis?"  
**Expected**: Agent uses RAG tool to search vector DB and give grounded answer

### Test 3: Study Material Generation ✅
**User**: "Create flashcards about photosynthesis"  
**Expected**: Agent uses flashcard generation tool

### Test 4: Presentation Creation ✅
**User**: "I want to create a presentation about photosynthesis"  
**Expected**: Agent recognizes need for presentation tool

---

## How to Run

### Step 1: Install Dependencies (2 minutes)
```bash
cd poc/07-langchain-agent
pip install -r requirements.txt
```

### Step 2: Run the Test (10-20 minutes)
```bash
python test_agent.py
```

**Note**: This will take 10-20 minutes because:
- Each LLM call takes 1-5 minutes on CPU
- Test has 4 different requests
- Be patient - it WILL complete!

### Step 3: Try Interactive Mode
```bash
python agent.py
```

Then type messages like:
- "What is photosynthesis?"
- "Create flashcards about cell biology"
- "Make a presentation about DNA"

---

## What You'll See

### Agent Reasoning Process
LangChain shows you what the agent is thinking:
```
> Entering new AgentExecutor chain...
I need to search the educational content.
Action: search_educational_content
Action Input: photosynthesis
Observation: Photosynthesis is the process...
Thought: I now have the answer
Final Answer: Based on the content...
```

This shows:
- ✅ Agent thinking process
- ✅ Which tool it decides to use
- ✅ Tool execution
- ✅ Final answer

---

## Expected Results

### Test 1: Simple Conversation
```
Agent responded: 2+2 equals 4.
[OK] Test 1 passed - Agent can converse
```

### Test 2: RAG Tool Usage
```
Agent uses search_educational_content tool
Answer: According to the uploaded content, photosynthesis is...
[OK] Test 2 passed - Agent can use RAG tool
```

### Test 3: Flashcard Tool
```
Agent uses generate_flashcards tool
Generated 5 flashcards on photosynthesis:
1. Q: What is the primary function...
[OK] Test 3 passed - Agent can generate flashcards
```

### Test 4: Presentation Recognition
```
Agent recognizes presentation request
Agent suggests: create_presentation tool
[OK] Test 4 passed - Agent recognizes presentation need
```

---

## Success Criteria

The POC is successful when:
- [x] Agent can have basic conversation
- [x] Agent uses RAG tool for grounded questions
- [x] Agent uses flashcard tool when requested
- [x] Agent recognizes presentation requests
- [x] Agent shows reasoning process

**If all pass**: Agent orchestration is WORKING ✅

---

## Troubleshooting

### Error: "No module named 'langchain'"
```bash
pip install langchain langchain-community langchain-ollama
```

### Error: "Connection refused to Ollama"
```bash
docker ps | grep ollama
# If not running:
cd old/Ella-Ai
docker-compose up -d ollama
```

### Error: "Collection 'education' not found"
```bash
# Load content first:
cd ../00-functional-poc
python test_full_workflow.py
# This loads photosynthesis content into ChromaDB
```

### Takes Too Long
**Normal**: Each LLM call is 1-5 minutes on CPU  
**Solution**: Be patient, or test on better hardware later

---

## After Testing

Once tests pass, you've proven:
1. ✅ LangChain agent works with Ollama
2. ✅ Agent can orchestrate your tools
3. ✅ Can build full chatbot on this foundation
4. ✅ Ready for backend integration

---

**Time**: 10-20 minutes for complete test  
**Result**: Will prove agent orchestration works!
