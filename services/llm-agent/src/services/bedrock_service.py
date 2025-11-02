"""
LLM Agent Service - Bedrock Service
AWS Bedrock integration for fast LLM responses
Ported from POC 07 - Tested and Validated with Claude 3 Sonnet
"""
import boto3
import json
from typing import List, Dict, Optional
from ..config import settings


class BedrockService:
    """Service for interacting with AWS Bedrock (Claude)"""
    
    def __init__(self):
        """Initialize Bedrock service"""
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
        Generate response from Bedrock Claude
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate (default: 2048)
            
        Returns:
            Generated text response
        """
        try:
            # Format prompt for Claude
            formatted_prompt = f"\n\nHuman: {prompt}\n\nAssistant:"
            
            # Prepare request body
            body = {
                "prompt": formatted_prompt,
                "temperature": temperature,
                "max_tokens_to_sample": max_tokens or 2048,
                "top_p": 0.9
            }
            
            # Call Bedrock API
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            return response_body.get('completion', '').strip()
            
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
