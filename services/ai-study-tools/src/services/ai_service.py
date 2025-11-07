"""
AI Service for generating study materials using AWS Bedrock
"""
import boto3
import json
from typing import List, Dict
from ..config import settings


class AIService:
    """AWS Bedrock service for AI generation"""
    
    def __init__(self):
        """Initialize Bedrock client"""
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"
    
    def generate_notes(self, source_content: str, source_type: str) -> Dict[str, str]:
        """
        Generate study notes from source content
        
        Args:
            source_content: The source material text
            source_type: Type of source (recording, photo, textbook)
            
        Returns:
            Dict with title and content
        """
        prompt = f"""You are an expert educational assistant. Generate comprehensive study notes from the following {source_type} content.

Create well-organized notes with:
- Clear title
- Key concepts and definitions
- Important points
- Examples if applicable
- Summary

Content:
{source_content}

Respond in JSON format:
{{
    "title": "Brief descriptive title",
    "content": "Detailed markdown-formatted notes"
}}"""
        
        response = self._generate(prompt)
        return json.loads(response)
    
    def generate_test(
        self,
        source_content: str,
        difficulty: str,
        question_count: int
    ) -> List[Dict]:
        """
        Generate test questions from source content
        
        Args:
            source_content: The source material text
            difficulty: easy, medium, or hard
            question_count: Number of questions to generate
            
        Returns:
            List of question dictionaries
        """
        prompt = f"""You are an expert educational assessment creator. Generate {question_count} {difficulty} difficulty test questions from the following content.

Create a mix of question types:
- Multiple choice (with 4 options)
- True/false
- Short answer

Content:
{source_content}

Respond in JSON format as an array of questions:
[
    {{
        "question_text": "Question here?",
        "question_type": "multiple_choice",
        "correct_answer": "Correct answer",
        "options": [{{"text": "Option A", "is_correct": false}}, ...],
        "explanation": "Why this is correct",
        "points": 1
    }}
]"""
        
        response = self._generate(prompt, max_tokens=4096)
        return json.loads(response)
    
    def generate_flashcards(
        self,
        source_content: str,
        card_count: int = 10
    ) -> List[Dict[str, str]]:
        """
        Generate flashcards from source content
        
        Args:
            source_content: The source material text
            card_count: Number of flashcards to generate
            
        Returns:
            List of flashcard dictionaries with front and back
        """
        prompt = f"""You are an expert educational content creator. Generate {card_count} flashcards from the following content.

Each flashcard should have:
- Front: A question or key term
- Back: The answer or definition

Content:
{source_content}

IMPORTANT: Respond ONLY with a valid JSON array. Do not include any markdown formatting, backticks, or explanatory text. Start directly with [ and end with ].

Example format:
[
    {{
        "front_text": "Question or term",
        "back_text": "Answer or definition"
    }}
]"""
        
        response = self._generate(prompt, max_tokens=2048)
        
        # Log response for debugging
        print(f"[DEBUG] Bedrock raw response: {response[:200]}")
        
        # Clean response - remove markdown formatting if present
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        # Parse JSON with error handling
        try:
            result = json.loads(cleaned)
            if not isinstance(result, list):
                raise ValueError(f"Expected list, got {type(result)}")
            return result
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parse failed: {e}")
            print(f"[ERROR] Cleaned response: {cleaned[:500]}")
            raise Exception(f"Failed to parse Bedrock response as JSON: {str(e)}")
    
    def _generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Generate text using Bedrock Converse API
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            messages = [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ]
            
            inference_config = {
                "temperature": temperature,
                "maxTokens": max_tokens,
                "topP": 0.9
            }
            
            response = self.client.converse(
                modelId=self.model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            
            output_message = response['output']['message']
            return output_message['content'][0]['text'].strip()
            
        except Exception as e:
            raise Exception(f"Bedrock generation failed: {e}")
