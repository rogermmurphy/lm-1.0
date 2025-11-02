"""
LLM Agent Service - AWS Bedrock Service
Fast cloud LLM alternative for testing
Uses Claude 3.5 Sonnet with Converse API for <10 second responses
"""
import boto3
from typing import Optional, List, Dict

from ..config import settings


class BedrockService:
    """AWS Bedrock service for fast LLM responses"""
    
    def __init__(self):
        """Initialize Bedrock client"""
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.model_id = settings.BEDROCK_MODEL
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text using Bedrock Converse API
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            # Use Converse API for Claude 3.5
            messages = [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
            
            # Prepare inference config
            inference_config = {
                "temperature": temperature,
                "maxTokens": max_tokens or 2048,
                "topP": 0.9
            }
            
            # Invoke model using Converse API
            response = self.client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            
            # Parse response
            output_message = response['output']['message']
            return output_message['content'][0]['text'].strip()
            
        except Exception as e:
            raise Exception(f"Bedrock generation failed: {e}")
    
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
            for msg in conversation_history[-5:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    history_text += f"Human: {content}\n\n"
                else:
                    history_text += f"Assistant: {content}\n\n"
        
        # Build prompt with or without context
        if context:
            system_message = "You are a helpful educational tutor. Answer the student's question using the information provided in the context below."
            prompt_text = f"{system_message}\n\nContext:\n{context}\n\n{history_text}Student: {message}\n\nTutor:"
        else:
            prompt_text = f"You are a helpful educational tutor.\n\n{history_text}Student: {message}\n\nTutor:"
        
        return self.generate(prompt_text)
