"""
RAG Chatbot - Answer questions using content from ChromaDB + Ollama
"""

import chromadb
from chromadb.config import Settings
import requests
import json
from typing import List, Dict, Optional

class RAGChatbot:
    def __init__(self, 
                 chroma_host="localhost", 
                 chroma_port=8000,
                 ollama_host="localhost",
                 ollama_port=11434,
                 model="llama3.2:3b"):
        """Initialize RAG chatbot"""
        self.client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(allow_reset=True)
        )
        self.ollama_url = f"http://{ollama_host}:{ollama_port}/api/generate"
        self.model = model
        print(f"[OK] RAG Chatbot initialized")
        print(f"  - ChromaDB: {chroma_host}:{chroma_port}")
        print(f"  - Ollama: {ollama_host}:{ollama_port}")
        print(f"  - Model: {model}")
    
    def search_content(self, query: str, collection_name="education", n_results=3) -> Dict:
        """Search for relevant content in ChromaDB"""
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"[ERROR] Error searching content: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def ask_ollama(self, prompt: str, stream=False) -> str:
        """Send prompt to Ollama and get response"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=300)
            response.raise_for_status()
            
            if stream:
                return response  # Return response object for streaming
            else:
                return response.json().get("response", "")
        except Exception as e:
            print(f"[ERROR] Error calling Ollama: {e}")
            return f"Error: {str(e)}"
    
    def answer_question(self, 
                       question: str, 
                       collection_name="education",
                       n_results=3,
                       include_sources=True) -> Dict:
        """Answer a question using RAG"""
        print(f"\nQuestion: {question}")
        
        # Step 1: Search for relevant content
        print(f"Searching for relevant content...")
        search_results = self.search_content(question, collection_name, n_results)
        
        documents = search_results['documents'][0] if search_results['documents'] else []
        metadatas = search_results['metadatas'][0] if search_results['metadatas'] else []
        distances = search_results['distances'][0] if search_results['distances'] else []
        
        if not documents:
            print("[WARNING] No relevant content found")
            return {
                "question": question,
                "answer": "I don't have enough information to answer that question. Please upload relevant educational content first.",
                "sources": [],
                "context_used": []
            }
        
        print(f"[OK] Found {len(documents)} relevant chunks")
        
        # Step 2: Build context from retrieved documents
        context = "\n\n---\n\n".join(documents)
        
        # Step 3: Create prompt for Ollama
        prompt = f"""You are a helpful educational tutor. Answer the student's question using ONLY the information provided in the context below. If the context doesn't contain enough information to answer the question, say so.

Context:
{context}

Question: {question}

Answer (be clear, educational, and cite specific facts from the context):"""
        
        # Step 4: Get answer from Ollama
        print(f"Asking Ollama...")
        answer = self.ask_ollama(prompt)
        
        # Step 5: Prepare response
        sources = []
        if include_sources and metadatas:
            for i, metadata in enumerate(metadatas):
                sources.append({
                    "source": metadata.get("source", "Unknown"),
                    "relevance_score": 1 - distances[i] if i < len(distances) else 0,
                    "chunk_index": metadata.get("chunk_index", i)
                })
        
        response = {
            "question": question,
            "answer": answer.strip(),
            "sources": sources,
            "context_used": documents if include_sources else []
        }
        
        print(f"[OK] Answer generated ({len(answer)} chars)")
        return response
    
    def chat_with_history(self, 
                         question: str,
                         history: List[Dict] = None,
                         collection_name="education") -> Dict:
        """Chat with conversation history"""
        if history is None:
            history = []
        
        # Search for relevant content
        search_results = self.search_content(question, collection_name, n_results=3)
        documents = search_results['documents'][0] if search_results['documents'] else []
        
        if not documents:
            context = "No specific context available."
        else:
            context = "\n\n".join(documents)
        
        # Build conversation history
        conversation = ""
        for msg in history[-3:]:  # Last 3 messages
            role = msg.get("role", "user")
            content = msg.get("content", "")
            conversation += f"{role.capitalize()}: {content}\n"
        
        # Create prompt
        prompt = f"""You are a helpful educational tutor. 

Context (use this to answer):
{context}

Conversation history:
{conversation}

Student: {question}

Tutor:"""
        
        answer = self.ask_ollama(prompt)
        
        return {
            "question": question,
            "answer": answer.strip(),
            "conversation_length": len(history)
        }

def main():
    """Test the RAG chatbot"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python rag_chatbot.py <question>")
        print('Example: python rag_chatbot.py "What is photosynthesis?"')
        sys.exit(1)
    
    question = " ".join(sys.argv[1:])
    
    # Create chatbot
    chatbot = RAGChatbot()
    
    # Answer question
    result = chatbot.answer_question(question)
    
    # Display result
    print(f"\n{'='*60}")
    print(f"QUESTION: {result['question']}")
    print(f"{'='*60}")
    print(f"\nANSWER:\n{result['answer']}")
    
    if result['sources']:
        print(f"\n{'='*60}")
        print(f"SOURCES:")
        for i, source in enumerate(result['sources'], 1):
            print(f"  {i}. {source['source']} (relevance: {source['relevance_score']:.2f})")
    
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
