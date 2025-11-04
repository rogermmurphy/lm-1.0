"""
Agent Service
Tool-using AI assistant with Bedrock Claude
Uses native tool calling instead of LangChain agents for compatibility
"""
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict, Any
import os
import json

from ..tools import list_user_classes, create_class_tool
from .rag_service import RAGService
from lm_common.logging import get_logger

logger = get_logger(__name__)


# System prompt
SYSTEM_PROMPT = """You are Little Monster's AI assistant. You help students manage their classes and study materials.

You have access to these tools that can execute actions:
- list_user_classes: List all classes for the current user
- create_class_tool: Create a new class (requires: name, optional: teacher_name, period, subject, color)

When the user asks to see their classes or create a class, use the appropriate tool.
For general questions, answer directly using your knowledge.
Always be helpful, clear, and encouraging."""


class AgentService:
    """Tool-using AI service with Bedrock Claude"""
    
    def __init__(self):
        """Initialize service with Bedrock Claude and tools"""
        logger.info("Initializing AgentService...")
        
        # Get AWS credentials from environment
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        bedrock_model = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
        
        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found in environment")
        
        # Initialize Bedrock LLM with tool binding
        logger.info(f"Connecting to AWS Bedrock ({bedrock_model})...")
        self.llm = ChatBedrock(
            model_id=bedrock_model,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
            model_kwargs={
                "temperature": 0.7,
                "max_tokens": 2048,
                "top_p": 0.9
            }
        )
        
        # Initialize tools
        self.tools = [
            list_user_classes,
            create_class_tool,
        ]
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Initialize RAG service for context
        self.rag_service = RAGService()
        
        logger.info("AgentService initialized successfully with tool binding")
    
    def chat(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        use_rag: bool = True
    ) -> str:
        """
        Process user message with tool calling
        
        Args:
            message: User message
            conversation_history: Previous conversation messages
            use_rag: Whether to use RAG context (default: True)
        
        Returns:
            Assistant response string
        """
        try:
            logger.info(f"Processing message: {message[:100]}...")
            
            # Get RAG context if enabled
            context = ""
            if use_rag:
                try:
                    context, sources = self.rag_service.get_context_for_query(message, n_results=3)
                    if context:
                        logger.info(f"Retrieved RAG context from {len(sources)} sources")
                        message = f"{message}\n\n[Context from study materials: {context[:500]}...]"
                except Exception as e:
                    logger.warning(f"RAG retrieval failed: {e}")
            
            # Build messages
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=message)
            ]
            
            # Invoke LLM with tools
            logger.info("Invoking LLM with tool binding...")
            response = self.llm_with_tools.invoke(messages)
            
            # Check if tool calls were made
            if hasattr(response, 'tool_calls') and response.tool_calls:
                logger.info(f"Tool calls detected: {len(response.tool_calls)}")
                
                # Execute tool calls
                tool_results = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_args = tool_call.get('args', {})
                    
                    logger.info(f"Executing tool: {tool_name}")
                    
                    # Find and execute tool
                    for tool in self.tools:
                        if tool.name == tool_name:
                            try:
                                result = tool.invoke(tool_args)
                                tool_results.append(result)
                            except Exception as e:
                                tool_results.append(f"Error executing {tool_name}: {str(e)}")
                            break
                
                # If we executed tools, return their results
                if tool_results:
                    return "\n\n".join(tool_results)
            
            # Return text response
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
            
        except Exception as e:
            logger.error(f"Error in agent chat: {str(e)}", exc_info=True)
            return f"I encountered an error processing your request: {str(e)}\n\nPlease try again or rephrase your question."
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [tool.name for tool in self.tools]
