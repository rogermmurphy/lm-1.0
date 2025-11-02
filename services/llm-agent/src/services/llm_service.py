"""
LLM Agent Service - LLM Service
Ollama LLM integration for chat completions
Extracted from POC 00 and POC 07 - Tested and Validated
"""
import requests
from typing import List, Dict, Optional
from ..config import settings


class LLMService:
    """Service for interacting with Ollama LLM"""
    
    def __init__(self):
        """Initialize LLM service"""
        self.ollama_url = f"{settings.OLLAMA_URL}/api/generate"
        self.model = settings.OLLAMA_MODEL
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            
            if max_tokens:
                payload["options"]["num_predict"] = max_tokens
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            
            return response.json().get("response", "")
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {e}")
    
    def chat_with_context(
        self,
        message: str,
        context: str = "",
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate chat response with optional context and history
        
        Args:
            message: User message
            context: Retrieved context from RAG
            conversation_history: Previous messages
            
        Returns:
            Assistant response
        """
        # Build conversation history
        history_text = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                history_text += f"{role.capitalize()}: {content}\n"
        
        # Build prompt
        if context:
            prompt = f"""You are a helpful educational tutor. Answer the student's question using the information provided in the context below.

Context:
{context}

{history_text}
Student: {message}

Tutor:"""
        else:
            prompt = f"""You are a helpful educational tutor.

{history_text}
Student: {message}

Tutor:"""
        
        return self.generate(prompt)
