# Functional POC: Educational AI Chatbot
## End-to-End Working Prototype

**Goal**: Build a working chatbot that can load educational content, answer questions, and generate study materials

**Time**: 2-3 days  
**Priority**: CRITICAL

---

## What We're Building

A **minimal but functional** system that demonstrates:

1. ✅ Load educational content (PDF, text, web pages) into vector database
2. ✅ Interactive chatbot that answers questions using that content (RAG)
3. ✅ Generate flashcards from the content
4. ✅ Generate quiz questions
5. ✅ Simple web interface to interact with it

**This proves the core use case before building the full app!**

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  Simple Web UI (HTML + JavaScript)         │
│  - Chat interface                           │
│  - Upload content                           │
│  - Generate flashcards/quizzes             │
└─────────────────────────────────────────────┘
                    │
                    ↓ HTTP
┌─────────────────────────────────────────────┐
│  FastAPI/Express Backend                    │
│  - /upload - Load content into vector DB   │
│  - /chat - Answer questions with RAG       │
│  - /flashcards - Generate flashcards       │
│  - /quiz - Generate quiz questions         │
└─────────────────────────────────────────────┘
        │                    │
        ↓                    ↓
┌──────────────┐    ┌──────────────────┐
│  ChromaDB    │    │  Ollama          │
│  (Content)   │    │  (GPT-OSS 20B)   │
│  Port 8000   │    │  Port 11434      │
└──────────────┘    └──────────────────┘
```

---

## Implementation Plan

### Phase 1: Content Loading (Day 1 Morning)

**Goal**: Load educational content into ChromaDB

**Files to Create**:
- `content_loader.py` - Load PDFs, text files, web pages
- `test_content/` - Sample educational materials
- `test_loader.py` - Test loading content

**Test**:
```python
# Load a biology chapter into ChromaDB
python content_loader.py test_content/biology_chapter1.pdf

# Query to verify it's loaded
python test_loader.py "What is photosynthesis?"
```

**Success**: Content is searchable in ChromaDB

---

### Phase 2: RAG Chatbot (Day 1 Afternoon)

**Goal**: Chat that answers questions using loaded content

**Files to Create**:
- `rag_chatbot.py` - Query ChromaDB + ask Ollama
- `test_chat.py` - Test question answering

**Test**:
```python
# Ask a question about loaded content
python test_chat.py "Explain the process of photosynthesis"

# Should return answer grounded in loaded content
```

**Success**: Chatbot answers questions using your content

---

### Phase 3: Study Material Generation (Day 2 Morning)

**Goal**: Generate flashcards and quizzes from content

**Files to Create**:
- `flashcard_generator.py` - Generate flashcards from topics
- `quiz_generator.py` - Generate quiz questions
- `test_generators.py` - Test generation

**Test**:
```python
# Generate flashcards on photosynthesis
python flashcard_generator.py "photosynthesis"

# Generate quiz questions
python quiz_generator.py "cell biology" --count 5
```

**Success**: Generates useful study materials

---

### Phase 4: Simple API (Day 2 Afternoon)

**Goal**: HTTP API for all functionality

**Files to Create**:
- `api.py` - FastAPI/Express endpoints
- `test_api.sh` - Test all endpoints

**Endpoints**:
```
POST /upload - Upload content
POST /chat - Ask questions
POST /flashcards - Generate flashcards
POST /quiz - Generate quiz
GET /collections - List loaded content
```

**Test**:
```bash
# Upload content
curl -X POST http://localhost:3000/upload \
  -F "file=@biology.pdf"

# Ask question
curl -X POST http://localhost:3000/chat \
  -d '{"question":"What is DNA?"}'

# Generate flashcards
curl -X POST http://localhost:3000/flashcards \
  -d '{"topic":"DNA replication","count":10}'
```

**Success**: All endpoints work

---

### Phase 5: Simple Web UI (Day 3)

**Goal**: Basic web interface to use the system

**Files to Create**:
- `index.html` - Simple chat interface
- `app.js` - Frontend logic
- `styles.css` - Basic styling

**Features**:
- Upload content button
- Chat input/output
- Generate flashcards button
- Generate quiz button
- Display results

**Test**: Open `index.html` in browser and use it

**Success**: Can upload content, chat, and generate materials via UI

---

## Directory Structure

```
poc/00-functional-poc/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── package.json               # Node dependencies (if using Express)
│
├── backend/
│   ├── content_loader.py      # Load content into ChromaDB
│   ├── rag_chatbot.py         # RAG implementation
│   ├── flashcard_generator.py # Generate flashcards
│   ├── quiz_generator.py      # Generate quizzes
│   ├── api.py                 # API server
│   └── config.py              # Configuration
│
├── frontend/
│   ├── index.html             # Web interface
│   ├── app.js                 # Frontend logic
│   └── styles.css             # Styling
│
├── test_content/              # Sample educational materials
│   ├── biology_chapter1.pdf
│   ├── math_notes.txt
│   └── history_article.md
│
└── tests/
    ├── test_loader.py
    ├── test_chat.py
    ├── test_generators.py
    └── test_api.sh
```

---

## Success Criteria

This POC is successful when you can:

1. ✅ Upload a PDF textbook chapter
2. ✅ Ask questions about it and get accurate answers
3. ✅ Generate 10 flashcards from the content
4. ✅ Generate a 5-question quiz
5. ✅ Do all this through a simple web interface
6. ✅ Response time is reasonable (< 5 seconds)

**If you can do this, the core concept is proven!**

---

## Technical Stack

**Backend**:
- Python + FastAPI (or Node.js + Express)
- ChromaDB client for vector operations
- Ollama client for LLM calls
- PyPDF2 or pdfplumber for PDF parsing

**Frontend**:
- Vanilla HTML/CSS/JavaScript (keep it simple)
- Fetch API for backend calls
- No framework needed for POC

**Infrastructure** (Already Running):
- Ollama (GPT-OSS 20B) - Port 11434
- ChromaDB - Port 8000

---

## Sample Code Snippets

### Content Loader Example

```python
# content_loader.py
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

def load_pdf_to_chroma(pdf_path, collection_name="education"):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # Connect to ChromaDB
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection(collection_name)
    
    # Add to ChromaDB
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk.page_content],
            ids=[f"doc_{i}"],
            metadatas=[{"source": pdf_path, "page": chunk.metadata.get("page", 0)}]
        )
    
    print(f"Loaded {len(chunks)} chunks from {pdf_path}")
```

### RAG Chatbot Example

```python
# rag_chatbot.py
import chromadb
import requests

def answer_question(question, collection_name="education"):
    # Connect to ChromaDB
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_collection(collection_name)
    
    # Search for relevant content
    results = collection.query(
        query_texts=[question],
        n_results=3
    )
    
    # Build context from results
    context = "\n\n".join(results['documents'][0])
    
    # Ask Ollama with context
    prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:"""
    
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'gpt-oss:20b',
        'prompt': prompt,
        'stream': False
    })
    
    return response.json()['response']
```

### Flashcard Generator Example

```python
# flashcard_generator.py
import requests

def generate_flashcards(topic, count=10):
    prompt = f"""Create {count} educational flashcards about {topic}.

Format each flashcard as:
Q: [Question]
A: [Answer]

Make them appropriate for high school students."""
    
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'gpt-oss:20b',
        'prompt': prompt,
        'stream': False
    })
    
    # Parse response into flashcard objects
    text = response.json()['response']
    flashcards = parse_flashcards(text)
    return flashcards

def parse_flashcards(text):
    # Parse Q:/A: format into structured data
    flashcards = []
    lines = text.split('\n')
    current_card = {}
    
    for line in lines:
        if line.startswith('Q:'):
            if current_card:
                flashcards.append(current_card)
            current_card = {'question': line[2:].strip()}
        elif line.startswith('A:') and current_card:
            current_card['answer'] = line[2:].strip()
    
    if current_card:
        flashcards.append(current_card)
    
    return flashcards
```

---

## Next Steps After POC

Once this functional POC works:

1. **Enhance**: Add more content types (websites, videos, images)
2. **Improve**: Better chunking, better prompts, better UI
3. **Scale**: Add user accounts, multiple collections, history
4. **Productionize**: Add error handling, logging, tests, deployment

But first, **prove the core concept works!**

---

## Why This Approach?

**Previous Attempt**: Built full application → Couldn't even log in → Failed

**This Approach**: 
- Build minimal working prototype first
- Prove core functionality works
- Then build full application around proven concept

**If this POC works, we know the full app will work!**

---

**Status**: Ready to Build  
**Next Step**: Start Phase 1 - Content Loading  
**Estimated Time**: 2-3 days to working prototype
