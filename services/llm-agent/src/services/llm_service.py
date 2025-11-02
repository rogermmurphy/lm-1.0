"""
LLM Agent Service - LLM Service
Unified LLM interface supporting both Ollama and AWS Bedrock
Switches between providers based on LLM_PROVIDER environment variable
"""
import requests
from typing import List, Dict, Optional
from ..config import settings
from .bedrock_service import BedrockService


class LLMService:
    """Unified service for interacting with LLMs (Ollama or Bedrock)"""
    
    def __init__(self):
        """Initialize LLM service with configured provider"""
        self.provider = settings.LLM_PROVIDER.lower()
        
        if self.provider == "bedrock":
            # Initialize Bedrock service
            self.bedrock_service = BedrockService()
            print(f"[LLM] Using AWS Bedrock ({settings.BEDROCK_MODEL})")
        else:
            # Initialize Ollama service
            self.ollama_url = f"{settings.OLLAMA_URL}/api/generate"
            self.model = settings.OLLAMA_MODEL
            self.bedrock_service = None
            print(f"[LLM] Using Ollama ({self.model})")
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from LLM (provider-agnostic)
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        if self.provider == "bedrock":
            # Use Bedrock
            return self.bedrock_service.generate(prompt, temperature, max_tokens)
        else:
            # Use Ollama
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
        Generate chat response with optional context and history (provider-agnostic)
        
        Args:
            message: User message
            context: Retrieved context from RAG
            conversation_history: Previous messages
            
        Returns:
            Assistant response
        """
        if self.provider == "bedrock":
            # Use Bedrock service's chat_with_context method
            return self.bedrock_service.chat_with_context(message, context, conversation_history)
        else:
            # Use Ollama with formatted prompt
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
